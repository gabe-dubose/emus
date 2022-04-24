#!/usr/bin/env python3

import argparse
from collections import Counter
from random import sample
import pandas as pd
import re

#define command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar="<Input Annotations>", 
    help = "List of annotated variants in .tsv format, where mutation classes are present in the first column")
parser.add_argument('-c', '--comparison', metavar="<Comparison Annotations>", 
    help = "List of annotated variants in .csv format for the input variants to be compared to")
parser.add_argument('-b', '--bootstraps', metavar = "<Number of bootstraps>", 
    help = "Number of times the comparison dataset is to be subsampled (number of bootstraps)")
parser.add_argument('-o', '--output', metavar = "<Output file name>", 
    help = "Handle for results files")
args = parser.parse_args()

class CompareVariants:
    def __init__(self, input, comparison):
        self.input = input
        self.comparison = comparison
    
    #function to retreive all annotations
    def get_annotations(input, comparison):
        mutations_annots = {}
        with open(comparison) as random:
            lines = random.readlines()
            for line in lines:
                mutation_name = line.split('\t')[0].rstrip().lstrip()
                if mutation_name not in mutations_annots:
                    mutations_annots[mutation_name] = list()
        with open(input) as input:
            lines = input.readlines()
            for line in lines:
                mutation_name = line.split('\t')[0].rstrip().lstrip()
                if mutation_name not in mutations_annots:
                    mutations_annots[mutation_name] = list() 
        return mutations_annots
    
    #function to read in comparisons
    def read_comparisons(comparison):
        comparison_mutations = []
        with open(comparison) as comparison:
            lines = comparison.readlines()
            for line in lines:
                header = bool(re.match("^#", line))
                if header == False:
                    mutation = line.split('\t')[0].rstrip().lstrip()
                    comparison_mutations.append(mutation)
        return comparison_mutations
    
    #function to read input
    def get_input_annotations(input_data_set):
        input_data = []
        with open(input_data_set) as input:
            lines = input.readlines()
            for line in lines:
                header = bool(re.match("^#", line))
                if header == False:
                    mutation_name = line.split('\t')[0].rstrip().lstrip()
                    input_data.append(mutation_name)
        return input_data

    #function to get bootstraps
    def get_bootstraps(bootstraps, sample_size, comparison_mutations, comparison_annotations, input_annotations):
        boot_annotations = CompareVariants.get_annotations(comparison_annotations, input_annotations) 
        for i in range(int(bootstraps)):
            random_sample = sample(comparison_mutations, sample_size)
            random_sample_counts = Counter(random_sample)
            for count in random_sample_counts:
                boot_annotations[count].append(random_sample_counts[count])
        return boot_annotations 
    
    #function to get probabilities
    def get_probabilities(frequencies, bootstraps):

        #initialize dictionaries to store counts for probabilities
        prob_positive = {}
        prob_negative = {}
        for mutation in input_frequencies:
            prob_positive[mutation] = 0
            prob_negative[mutation] = 0
        
        for mutation in input_frequencies:
            comparison = bootstrap_comparisons[mutation]
            obs = input_frequencies[mutation]
            for comp in comparison:
                #input is greater than comparison
                if obs >= comp:
                    prob_positive[mutation] += 1
                #input is less than comparison
                if obs <= comp:
                    prob_negative[mutation] += 1
            
        for num in prob_positive:
            prob_positive[num] = prob_positive[num]/int(bootstraps)
        for num in prob_negative:
            prob_negative[num] = prob_negative[num]/int(bootstraps)
        
        return (prob_positive, prob_negative)
       
#read input
input_data = CompareVariants.get_input_annotations(args.input)

#read comparison
comparison_mutations = CompareVariants.read_comparisons(args.comparison)

#get bootstraps
input_size = len(input_data)
bootstrap_comparisons = CompareVariants.get_bootstraps(bootstraps=args.bootstraps, sample_size=input_size, comparison_mutations=comparison_mutations, 
    comparison_annotations=args.comparison, input_annotations=args.input)

#define comparison data and initial frequencies
comparison_df = pd.DataFrame(list(bootstrap_comparisons.values()), index=bootstrap_comparisons.keys()).transpose()
input_frequencies = Counter(input_data)

#get probability results
probs = CompareVariants.get_probabilities(input_frequencies, args.bootstraps)
probs_greater = probs[0]
probs_less = probs[1]

#write results
output_file = f"{args.output}.tsv"
with open(output_file, 'a') as output:
    output.write(f'Mutation\tP(Obs>=Sim)\tP(Obs<=Sim)\n')
    for result in probs_greater:
        output.write(f"{result}\t{probs_greater[result]}\t{probs_less[result]}\n")

    #output.write(f'P(Observed >= Simulation)\n')
    #for result in probs_greater:
        #output.write(f"{result}\t{probs_greater[result]}\n")
    #output.write(f'\n')
    #output.write(f'P(Observed <= Simulation)\n')
    #for res in probs_less:
        #output.write(f"{res}\t{probs_less[res]}\n")

#write datafile for plotting
with open(f'{args.output}.bootstraps.tsv', 'a') as datafile:
    datafile.write('#Mutation\tObserved\tBootstraps\n')
for mutation in input_frequencies:
    bootstraps = bootstrap_comparisons[mutation]
    bootstraps_out = ''
    for boot in bootstraps:
        bootstraps_out = bootstraps_out + f'{boot},'
    observed = input_frequencies[mutation]
    with open(f'{args.output}.bootstraps.tsv', 'a') as datafile:
        datafile.write(f'{mutation}\t{observed}\t{bootstraps_out.rstrip()}\n')