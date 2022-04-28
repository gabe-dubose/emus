#!/usr/bin/env python3

import re
import argparse

#get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar = '<Input file>', 
    help = "Input annotation file")
parser.add_argument('--snpeff', action = 'store_true', 
    help = "Use if annotation file is an SnpEff VCF file")
parser.add_argument('--annovar', action = 'store_true', 
    help = "Use if annotation file is the standard ANNOVAR .csv output")
parser.add_argument('--vep', action = 'store_true', 
    help = "Use if annotation file is the VEP .tsv output")
parser.add_argument('-o', '--output', metavar = "<Outfile.tsv>", 
    help = "Output file name")
args = parser.parse_args()

class GetAnnotations:
    def __init__(self, file):
        self.file = file

    def read_snpeff_vcf(file, output):
        non_count = 0
        with open(output, 'a') as outfile:
            outfile.write(f'#ANNOTATION\n')
        
        with open(file, 'r') as infile:
            lines = infile.readlines()
            for line in lines:
                metadata = bool(re.match('#', line))
                if metadata == False:
                    try:
                        info = line.split('\t')[7]
                        annotation = info.split('|')[1]
                        with open(args.output, 'a') as outfile:
                            outfile.write(f'{annotation}\n')
                    except:
                        non_count += 1
        
            if non_count != 0:
                print(f'WARNING: {non_count} varinat annotations were not found.')
    
    def read_annovar_vars(file, output):
        non_count = 0
        with open(output, 'a') as outfile:
            outfile.write(f'#ANNOTATION\n')

        with open(file, 'r') as infile:
            lines = infile.readlines()
            count = 0 
            for line in lines:
                header = bool(re.match('Chr,Start', line))
                if header == False:
                    try:
                        annotation = line.split(',')[8]
                        if len(annotation) != 1:
                            with open(args.output, 'a') as outfile:
                                annotation = annotation.replace(" ", "_")
                                annotation = annotation.rstrip('"').lstrip('"')
                                print(annotation)
                                outfile.write(f'{annotation}\n')
                    except:
                        non_count += 1

            if non_count != 0:
                print(f'WARNING: {non_count} varinat annotations were not found.')               

    def read_vep_vars(file, output):
        non_count = 0
        with open(output, 'a') as outfile:
            outfile.write(f'#ANNOTATION\n')

        with open(file, 'r') as infile:
            lines = infile.readlines()
            for line in lines:
                try:
                    annotation = line.split('\t')[6]
                    with open(args.output, 'a') as outfile:
                        outfile.write(f'{annotation}\n')
                except:
                    non_count += 1

            if non_count != 0:
                print(f'WARNING: {non_count} varinat annotations were not found.')   

#get annotations
if args.snpeff == True:
    annotations = GetAnnotations.read_snpeff_vcf(args.input, args.output)

if args.annovar == True:
    annotations = GetAnnotations.read_annovar_vars(args.input, args.output)

if args.vep == True:
    annotations = GetAnnotations.read_vep_vars(args.input, args.output)
