#!/usr/bin/env python3

import argparse
import re
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar = '<Input VCF File>', 
    help = "VCF file for variant distribution plotting; a separate plot will be made for each unique sequence ID")
parser.add_argument('-o', '--outdir', metavar='<Directory name>', 
    help = "Directory to save histogram plots to")
args = parser.parse_args()

class VariantData:
    def __init__(self, data):
        self.data = data
        
    #function to get variant positions for each sequence
    def extract_data(self, data):
        variant_positions = {}
        with open(data, 'r') as datafile:
            lines = datafile.readlines()
            for line in lines:
                metadata = bool(re.match("^#", line))
                if metadata == False:
                    sequence_id = line.split('\t')[0]
                    position = line.split('\t')[1]
                    if sequence_id not in variant_positions:
                        variant_positions[sequence_id] = []
                    variant_positions[sequence_id].append(position)

        return variant_positions

#define variant data object and get data
variants_data = VariantData(args.input)
variant_positions = variants_data.extract_data(args.input)

#plot variant histograms
for sequence in variant_positions:
    data = [int(x) for x in variant_positions[sequence]]

    plt.figure(figsize=(10,5)).tight_layout()
    plt.grid(zorder=1)
    plt.hist(data, 100, color = 'lightsalmon', zorder = 2)
    plt.margins(x=0)
    plt.title(f'{sequence}')   
    pdf = f"{args.outdir}/{sequence}_hist.pdf"
    plt.savefig(pdf)