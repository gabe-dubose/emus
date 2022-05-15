#!/usr/bin/env python3

import argparse
import random
from datetime import date
import time
import pyfaidx

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar = '<Input Genome in FASTA Format>', 
    help = "Genome sequence used to simulate null distribution of mutaitons")
parser.add_argument('-s', '--snp', metavar = '<Whole Number>', type = int,
    help = "Number of SNPs to simualte in input genome")
parser.add_argument('-o', '--output', metavar = '<output_file.vcf>', 
    help = "Handle that will be added to the output VCF file")
args = parser.parse_args()

class GenomeSequence:
    def __init__(self, genome):
        self.genome = genome
    
    def simulate_variants(self, fasta, number):

        #read fasta file
        genome = pyfaidx.Fasta(fasta)
        sequences = list(genome.keys())
        
        alphabet = ['A', 'T', 'G', 'C']

        mutation_count = 0
        mutation_info = {}
        variant_calls = []

        while mutation_count < number:
            variant = random.choices(alphabet, k=1)
            variant = variant[0]
            seqid = random.choices(sequences, k=1)
            seqid = seqid[0]
            position = random.randint(0, len(genome[seqid]) - 1)
            original = str(genome[seqid][position]).upper()
        
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

    
def write_vcf(fasta, variants):
    #read fasta file
    genome = pyfaidx.Fasta(fasta)
    sequences = genome.keys()

    #initialize output VCF
    today = date.today().strftime("%Y%m%d")
    with open(args.output, 'a') as outfile:
        outfile.write(f'##fileformat=VCFv4.3\n')
        outfile.write(f'##date={today}\n')
        outfile.write(f'##source=emus.v.1.0.0\n')
        outfile.write(f'##reference={args.input}\n')
        for sequence in sequences:
            outfile.write(f'##contig=<ID={sequence}, lenght = {len(genome[sequence])}>\n')

        outfile.write(f'#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\tSAMPLE\n')

        sorted_variants = sorted(variants, key=lambda x: (x[0], x[1]))
        for variant in sorted_variants:
            var_line = f'{variant[0]}\t{int(variant[1])+1}\t.\t{variant[2]}\t{variant[3]}\t.\t.\t.\tGT\t1\n'
            outfile.write(var_line)

#define sequence objects
sequence_object = GenomeSequence(args.input) 

#simulate mutations
print('Simulating mutations...')
start_sim = time.time()
simulation = sequence_object.simulate_variants(args.input, args.snp)
print(f'Done in {time.time() - start_sim} seconds.')

#write variant call file
print('Writing variant call file...')
write_vcf(args.input, simulation)
print('Done.')