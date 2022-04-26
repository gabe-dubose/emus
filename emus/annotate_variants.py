#!/usr/bin/env python3

import os
import argparse

#get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar = '<VCF File>',
    help = "Variant call file to be annotated")
parser.add_argument('-r', '--reference', metavar = '<Reference Database>', 
    help = 'Genome databse to be used in variant annotaiton')
parser.add_argument('-o', '--output', metavar = '<Output_file.vcf>', 
    help = "Handle for outputfile")
args = parser.parse_args()

#Class to annotate variants
class AnnotateVariants:
    def __init__(self, vcf, genome):
        self.vcf = vcf
        self.genome = genome

    #function to get variant annotations
    def get_variant_annotations():

        print('Locating config:')
        #locate snpeff bin by looking for its symlink
        snpeff_exe = os.popen('which snpeff').read().rstrip()
        snpeff_path = os.popen(f'ls -lia {snpeff_exe}').read().rstrip().split()
        snpeff_bin = snpeff_path[9].split('/')[1:-1]
        snpeff_bin_path = ''
        for dir in snpeff_bin:
            snpeff_bin_path = snpeff_bin_path + f'/{dir.rstrip()}'
        
        #locate path to main dir by tracing back simlink
        snpeff_link = snpeff_path[-1].split('/')[0:-1]
        snpeff_main_path = ''
        for dir in snpeff_link:
            snpeff_main_path = snpeff_main_path + f'/{dir}'
        path_to_main_snpeff = snpeff_bin_path + snpeff_main_path

        config = os.popen(f'ls {path_to_main_snpeff}/snpeff.config').read().rstrip()

        print(f'config found at {config}')

        print('Annotating Variants...')
        os.system(f'snpeff eff -c {config} {args.reference} {args.input} > {args.output}')
     
#annotate variants
AnnotateVariants.get_variant_annotations()

