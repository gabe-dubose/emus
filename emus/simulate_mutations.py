#!/usr/bin/env python3

import argparse
import re
import random
from datetime import date
import time

#define command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar = '<Input Genome in FASTA Format>', 
    help = "Genome sequence used to simulate null distribution of mutaitons")
parser.add_argument('-s', '--snp', metavar = '<Whole Number>', type = int,
    help = "Number of SNPs to simualte in input genome")
parser.add_argument('-o', '--output', metavar = '<output_file.vcf>', 
    help = "Handle that will be added to the output VCF file")
args = parser.parse_args()

#class to handle initial input genome sequence and simulate mutations
class GenomeSequence:
    def __init__(self, genome):
        self.genome = genome
    
    #function to extract raw genomes sequences for each chromosome
    def get_genome(self, genome):
        
        raw_sequence = {}
        current_header = ''
        with open(genome) as genome:
            lines = genome.readlines()
            for line in lines:
                line = line.rstrip()
                header_line = bool(re.match("^>", line))
                if header_line == True:
                    current_header = line.lstrip('>')
                    current_header = current_header.split(' ')[0]
                    raw_sequence[current_header] = ''
                else:
                    raw_sequence[current_header] = raw_sequence[current_header] + line.upper()

        #get sequence length information to be written to VFC file later
        sequence_data = {}
        for seq in raw_sequence:
            sequence_data[seq] = len(raw_sequence[seq])

        sequences_information = (raw_sequence, sequence_data)
        return sequences_information

    #function to simualte mutations in genome
    def simulate_mutations(self, sequence_dict, number):
        alphabet = ['A', 'T', 'G', 'C']

        #get sequence ids
        sequence_headers = []
        for key in sequence_dict:
            sequence_headers.append(key)
        
        #loop to generate random mutations
        variant_calls = []
        mutation_info = {}
        mutation_count = 0
        while mutation_count < number:

            variant = str(random.sample(alphabet, 1)).lstrip("['").rstrip("]'")
            seqid = str(random.sample(sequence_headers, 1)).lstrip("['").rstrip("]'")
            position = random.randint(0, len(sequence_dict[seqid]) - 1)
            original =  sequence_dict[seqid][position]

            #add sequence id to info dictionary if not already there
            if seqid not in mutation_info:
                mutation_info[seqid] = []

            #check if the variant is the same as the original and if that position had already been simulated
            #if conditions are met, place variant
            if variant != original and position not in mutation_info[seqid]:
                variant_call = [seqid, position, original, variant]
                variant_calls.append(variant_call)
                mutation_info[seqid].append(position)
                mutation_count += 1
        
        return variant_calls

#function to write vcf file
def write_vcf(variants, seq_data):
    today = date.today().strftime("%Y%m%d")
    with open(args.output, 'a') as outfile:
        outfile.write(f'##fileformat=VCFv4.3\n')
        outfile.write(f'##date={today}\n')
        outfile.write(f'##source=emus.v.1.0.0\n')
        outfile.write(f'##reference={args.input}\n')
        
        for seq in seq_data:
            outfile.write(f'##contig=<ID={seq},lenght={seq_data[seq]}>\n')

        outfile.write(f'#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n')

        #sorting variants by chromosome and position
        sorted_variants = sorted(variants, key=lambda x: (x[0], x[1]))
        for variant in sorted_variants:
            var_line = f'{variant[0]}\t{int(variant[1])+1}\t.\t{variant[2]}\t{variant[3]}\t.\t.\t.\tGT\t1\n'
            outfile.write(var_line)

#define sequence objects
sequence_object = GenomeSequence(args.input) 

#extract raw sequences and sequences data
print('Reading Sequences...')
start_read = time.time()
sequence_information = sequence_object.get_genome(args.input)
raw_sequence = sequence_information[0]
sequence_data = sequence_information[1]
print(f'Done in {time.time() - start_read} seconds.')

#simulate mutations
print('Simulating mutations...')
start_sim = time.time()
simulation = sequence_object.simulate_mutations(raw_sequence, args.snp)
print(f'Done in {time.time() - start_sim} seconds.')

#write variant call file
print('Writing variant call file...')
write_vcf(simulation, sequence_data)
print('Done.')