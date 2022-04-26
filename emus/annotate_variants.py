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
        print('Annotating Variants...')
        os.system(f'snpeff eff {args.reference} {args.input} > {args.output}')
     
#annotate variants
AnnotateVariants.get_variant_annotations()

