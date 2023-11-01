#!/usr/bin/env python3

import argparse
from collections import Counter
from random import sample
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Set up command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar="<Input Annotations>", 
    help = "List of annotated variants in .csv format, where mutation classes are present in the first column")
parser.add_argument('-c', '--comparison', metavar="<Comparison Annotations>", 
    help = "List of annotated variants in .csv format for the input variants to be compared to, typically simulated mutations")
parser.add_argument('-b', '--bootstraps', metavar = "<Number of bootstraps>", 
    help = "Number of times the comparison dataset is to be subsampled (number of bootstraps)")
parser.add_argument('-o', '--output', metavar = "<Output file name>", 
    help = "Handle for results files")
parser.add_argument('-p', '--plot', action = 'store_true',
    help = "Plot histogram of bootstrap analysis. Note: This may produce a lot of plots, depending on how many mutational classes you have")
args = parser.parse_args()

#function to retreive all mutation annotations
def get_annotations(input, comparison):
    mutations_annots = {}
    with open(comparison) as random:
        lines = random.readlines()
        for line in lines:
            mutation_name = line.split(",")[0].rstrip().lstrip()
            if mutation_name not in mutations_annots:
                mutations_annots[mutation_name] = list()
    with open(input) as input:
        lines = input.readlines()
        for line in lines:
            mutation_name = line.split(",")[0].rstrip().lstrip()
            if mutation_name not in mutations_annots:
                mutations_annots[mutation_name] = list() 
    return(mutations_annots) 

#read comparison mutations
comparison_mutations = []
with open(args.comparison) as comparison:
    lines = comparison.readlines()
    for line in lines:
        mutation = line.split(",")[0].rstrip().lstrip()
        comparison_mutations.append(mutation)

#function to take n random samples (bootstraps) of size k (sample size)
def get_bootstraps(bootstraps, sample_size, comparison_mutations, comparison_annotations, input_annotations):
    total_annotations = get_annotations(comparison_annotations, input_annotations) 
    for i in range(int(bootstraps)):
        random_sample = sample(comparison_mutations, sample_size)
        random_sample_counts = Counter(random_sample)
        for count in random_sample_counts:
            total_annotations[count].append(random_sample_counts[count])
    return(total_annotations)

#function to read in input dataset for comparison
def input_annotations(input_data_set):
    input_data = []
    with open(input_data_set) as input:
        lines = input.readlines()
        for line in lines:
            mutation_name = line.split(",")[0].rstrip().lstrip()
            input_data.append(mutation_name)
    return(input_data)

#read in input data
input_data = input_annotations(args.input)

#perform bootstrapping
input_size = len(input_data)
bootstrap_comparisons = get_bootstraps(bootstraps=args.bootstraps, sample_size=input_size, comparison_mutations=comparison_mutations, 
    comparison_annotations=args.comparison, input_annotations=args.input)

comparison_df = pd.DataFrame(list(bootstrap_comparisons.values()), index=bootstrap_comparisons.keys()).transpose()

#get initial input frequencies for each mutations class
input_frequencies = Counter(input_data)

#Evaluate bootstrapping results:
#Initialize dictionaries to store counts for probabilities
prob_positive = {}
prob_negative = {}
for mutation in input_frequencies:
    prob_positive[mutation] = 0
    prob_negative[mutation] = 0

#Count number of times input is greater than or less than comparison and divide by bootstraps
for mutation in input_frequencies:
    comparison = bootstrap_comparisons[mutation]
    obs = input_frequencies[mutation]
    for comp in comparison:
        #input is greater than comparison
        if obs > comp:
            prob_positive[mutation] += 1
        #input is less than comparison
        if obs < comp:
            prob_negative[mutation] += 1

for num in prob_positive:
    prob_positive[num] = prob_positive[num]/int(args.bootstraps)

for num in prob_negative:
    prob_negative[num] = prob_negative[num]/int(args.bootstraps)

#write results to output file
output_file = f"{args.output}.csv"
with open(output_file, 'a') as output:
    output.write(f'P(Input > Comparison)\n')
    for result in prob_positive:
        output.write(f"{result},{prob_positive[result]}\n")
    output.write(f'\n')
    output.write(f'P(Input < Comparison)\n')
    for res in prob_negative:
        output.write(f"{res},{prob_negative[res]}\n")

#make histograms displaying results of bootstrap analysis, if user specifies
if args.plot == True:
    for mutation in input_frequencies:
        fig = plt.figure(figsize=(5,5)).tight_layout()
        data = comparison_df[mutation]
        sns.histplot(data=data, kde=True, color='blue', alpha=0.5)
        plt.axvline(x = input_frequencies[mutation], color='red', linewidth = 5)
        plt.tight_layout()
        pdf = f"{args.output}_{mutation}.pdf"
        plt.savefig(pdf)
        