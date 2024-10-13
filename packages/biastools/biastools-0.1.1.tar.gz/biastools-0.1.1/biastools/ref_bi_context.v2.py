import argparse
import re
import pickle
from os import path
import pysam
import numpy as np
from scipy.stats import chisquare
from typing import List, Tuple, Dict, Union
from collections import defaultdict
import logging

# Constants
PADDING = 5
VAR_CHAIN = 25
EXTEND_LIMIT = 70

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VariantAnalyzer:
    def __init__(self, vcf_file: str, sam_file: str, fasta_file: str, padding: int = PADDING, var_chain: int = VAR_CHAIN):
        self.f_vcf = pysam.VariantFile(vcf_file)
        self.f_sam = pysam.AlignmentFile(sam_file)
        self.f_fasta = pysam.FastaFile(fasta_file)
        self.padding = padding
        self.var_chain = var_chain
        self.dict_ref_haps = defaultdict(dict)
        self.dict_ref_gaps = defaultdict(dict)
        self.dict_ref_cohorts = defaultdict(dict)
        self.dict_set_conflict_vars = defaultdict(set)
        
    def analyze(self):
        self.build_variant_maps()
        self.compare_reads_to_variants()
        self.generate_report()
    
    def build_variant_maps(self):
        logger.info("Start building the variant maps...")
        self.dict_set_conflict_vars, self.dict_ref_haps, self.dict_ref_cohorts, self.dict_ref_gaps = self.variant_seq()
        
        # Extend conflict set
        for ref_name, positions in self.dict_set_conflict_vars.items():
            for pos in list(positions):
                self.dict_set_conflict_vars[ref_name].update(range(pos - self.var_chain, pos + self.var_chain + 1))
    
    def compare_reads_to_variants(self):
        logger.info("Start comparing reads to the variant map...")
        self.dict_ref_bias = self.compare_sam_to_haps()
    
    def generate_report(self):
        logger.info("Start output report...")
        self.output_report()

    def fetch_alt_seqs(self, var: pysam.VariantRecord, ref: str) -> List[str]:
        """
        Generate alternative sequences for a given variant.

        Args:
            var: Variant record
            ref: Reference sequence

        Returns:
            List of alternative sequences
        """
        return [ref[:var.start] + alt + ref[var.stop:] for alt in var.alts]

    def parse_MD(self, md_tag: str) -> List[Tuple[str, Union[int, str]]]:
        """
        Parse the MD tag from a SAM alignment.

        Args:
            md_tag: MD tag string

        Returns:
            List of tuples representing operations in the MD tag
        """
        md_parts = re.split('(\d+)', md_tag)
        md_chunks = []
        for part in md_parts:
            if part.isdigit():
                md_chunks.append(('M', int(part)))
            elif part.startswith('^'):
                md_chunks.append(('D', part[1:]))
            elif part:
                md_chunks.append(('m', part))
        return md_chunks

    def map_read_to_ref(self, read_start: int, read_end: int, cigar_tuples: List[Tuple[int, int]]) -> Dict[int, int]:
        """
        Map read positions to reference positions based on CIGAR string.
        
        Args:
            read_start: Starting position of the read on the reference
            read_end: Ending position of the read on the reference
            cigar_tuples: List of CIGAR operations
        
        Returns:
            Dictionary mapping reference positions to read positions
        """
        dict_read_map = {}
        ref_cursor = read_start
        read_cursor = 0
        for code, runs in cigar_tuples:
            if code in (0, 7, 8):  # M or = or X
                for pos in range(ref_cursor, ref_cursor + runs):
                    dict_read_map[pos] = read_cursor
                    read_cursor += 1
                ref_cursor += runs
            elif code == 1:  # I
                dict_read_map[ref_cursor] = read_cursor
                ref_cursor += 1
                read_cursor += runs
            elif code == 2:  # D
                for pos in range(ref_cursor, ref_cursor + runs):
                    dict_read_map[pos] = read_cursor
                read_cursor += 1
                ref_cursor += runs
            elif code in (4, 5):  # S or H, pysam already parsed
                pass
            else:
                logger.error(f"Unexpected CIGAR code {code} in sequence {self.query_name}")
        return dict_read_map

    def chi_square_test(self, var_start: int, list_pos_start: List[int]) -> float:
        """
        Perform chi-square test on the distribution of read start positions.

        Args:
            var_start: Variant start position
            list_pos_start: List of read start positions

        Returns:
            p-value of the chi-square test
        """
        if len(list_pos_start) < 2:
            return 0
        bucket_num = 5
        bucket_len = int(100 / bucket_num)
        list_count = np.zeros(bucket_num)
        input_idx = np.minimum((var_start - np.array(list_pos_start)) // bucket_len, bucket_num - 1)
        np.add.at(list_count, input_idx, 1)
        _, p_value = chisquare(list_count)
        return 0 if np.isnan(p_value) else p_value

    def output_report(self):
        logger.info("Generating output report...")
        
        with open(self.args.out, 'w') as f_out:
            self._write_header(f_out)
            self._write_variant_data(f_out)
        
        logger.info("Output report generated successfully.")

    def _write_header(self, f_out):
        f_out.write("##fileformat=VCFv4.2\n")
        f_out.write("##INFO=<ID=REF_BIAS,Number=1,Type=Float,Description=\"Reference bias score\">\n")
        f_out.write("##INFO=<ID=CHI_SQUARE,Number=1,Type=Float,Description=\"Chi-square test p-value\">\n")
        f_out.write("##INFO=<ID=READ_DEPTH,Number=1,Type=Integer,Description=\"Total read depth\">\n")
        f_out.write("##INFO=<ID=ALT_DEPTH,Number=1,Type=Integer,Description=\"Alternative allele depth\">\n")
        f_out.write("#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n")

    def _write_variant_data(self, f_out):
        for ref_name in self.dict_ref_bias:
            for var_pos in sorted(self.dict_ref_bias[ref_name]):
                var_data = self.dict_ref_bias[ref_name][var_pos]
                ref_allele = var_data['ref']
                alt_allele = var_data['alt']
                ref_bias = var_data['ref_bias']
                chi_square = var_data['chi_square']
                read_depth = var_data['read_depth']
                alt_depth = var_data['alt_depth']
                
                info = f"REF_BIAS={ref_bias:.4f};CHI_SQUARE={chi_square:.4f};READ_DEPTH={read_depth};ALT_DEPTH={alt_depth}"
                f_out.write(f"{ref_name}\t{var_pos}\t.\t{ref_allele}\t{alt_allele}\t.\t.\t{info}\n")

# ... (other methods would be implemented here)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Analyze reference bias in genomic sequencing data.")
    parser.add_argument('-v', '--vcf', help='VCF file', required=True)
    parser.add_argument('-s', '--sam', help='SAM file', required=True)
    parser.add_argument('-f', '--fasta', help='Reference FASTA file', required=True)
    parser.add_argument('-r', '--real_data', help='Turn off hap_information warning for real data', action='store_true')
    parser.add_argument('-p', '--golden_pickle', help='Pickle file containing the golden information for report reference')
    parser.add_argument('-t', '--run_id', help='Tag for run_id, can be used to indicate chromosome number')
    parser.add_argument('-o', '--out', help='Output file', required=True)
    return parser.parse_args()

if __name__ == "__main__":
    try:
        args = parse_arguments()
        analyzer = VariantAnalyzer(args.vcf, args.sam, args.fasta)
        analyzer.analyze()
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise
