#!/usr/bin/env python3

import re
import argparse

#get commandline arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar = '<VCF File>', 
    help = 'VCF File that will have relevant information extracted')
parser.add_argument('-o', '--output', metavar = '<Output handle>', 
    help = 'Prefix to add to output .tsv file')
args = parser.parse_args()

class ReadVCF:
    def __init__(self, vcf):
        self.vcf = vcf

    #function to get annotation information from VCF info
    def get_annotations(vcf):
        non_count = 0
        with open(args.output, 'a') as outfile:
            outfile.write(f'#ANNOTATION\tCHROMOSOME\tPOSITION\tEFFECT\tVARIANT\n')

        with open(args.input, 'r') as vcf:
            lines = vcf.readlines()
            for line in lines:
                metadata = bool(re.match('#', line))
                if metadata == False:
                    try:
                        chrom = line.split('\t')[0]
                        position = line.split('\t')[1]
                        info = line.split('\t')[7]
                        annotation = info.split('|')[1]
                        effect = info.split('|')[2]
                        var = info.split('|')[9]
                        with open(args.output, 'a') as outfile:
                            outfile.write(f'{annotation}\t{chrom}\t{position}\t{effect}\t{var}\n')
                    except:
                        non_count += 1

            if non_count != 0:
                print(f'Warning: {non_count} varinats were not annotated.')

#get annotation information
annotations = ReadVCF.get_annotations(args.input)
