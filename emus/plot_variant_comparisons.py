#!/usr/bin/env python3

import argparse
import re
import matplotlib.pyplot as plt
import seaborn as sns
import statistics

#define command line arguments
parser = argparse.ArgumentParser()

#required input
parser.add_argument('-i', '--input', metavar = '<Input Data>', required = True,
    help = "_boostraps.tsv file generated in previous step")
parser.add_argument('-o', '--outdir', metavar = '<Direcotry Name>', required = True,
    help = "Directory to write output plots")

#plotting options
parser.add_argument('--hist', action = 'store_true',
    help = "Plot histogram of bootstraps")
parser.add_argument('--kde', action = 'store_true', 
    help = "Plot kernel density estimate plot of bootstraps")
parser.add_argument('--ecdf', action = 'store_true', 
    help = "Plot emperical cumulative distribution function of bootstraps")

#plot additions
parser.add_argument('--cdf', action = 'store_true', required = False,
    help= "add cumulative density function to plot")
parser.add_argument('--color_tail', action = 'store_true', required = False,
    help = "Shade in area under curve that corresponds to the part of the distribution that is greater than or less than the median. Default color: tab:orange.")

#styling options
parser.add_argument('--comp_line_color', default = 'tab:orange', 
    help = "Color comparison line. Default = tab:orange")
parser.add_argument('--plot_color', default = 'tab:blue', 
    help = "Color for histogram, kde, or ecdf plot")
parser.add_argument('--blank_bars', action = 'store_true',
    help = "Make bars solid color as opposed to empty")
parser.add_argument('--background_theme', default = 'white',
    help = "Change plot background color. Options: white, dark")

args = parser.parse_args()

#class to plot comparisons
class PlotComparisons:
    def __init__(self, input):
        input = self.input
    
    #function to make histogram
    def histogram_plot(mutation, observed, bootstraps):

        sns.set_style(args.background_theme)
        plt.figure(figsize=(5,5)).tight_layout()
        plt.margins(x=0)
        data = [int(x) for x in bootstraps]
        
        ax = sns.histplot(data=data, discrete = True, color = args.plot_color)
        plt.axvline(x = observed, color=args.comp_line_color, linewidth = 3)

        #add kde: Always need kde for coloring tail, but don't want to make it visible if kde argument isn't specified 
        if args.kde == True and args.cdf == True:
            alpha = 0
        if args.kde == False:
            alpha = 0
        if args.kde == True and args.cdf == False:
            alpha = 1
        #add kde
        ax2 = ax.twinx()
        sns.kdeplot(data=data, color = args.plot_color, alpha = alpha, ax = ax2, linewidth = 3, warn_singular=False)
        ax2.set(ylabel=None)
        ax2.tick_params(right=False)
        ax2.set(yticklabels=[])

        #add cdf if specified
        if args.cdf == True:
            ax3 = ax.twinx()
            sns.kdeplot(data=data, cumulative = True, ax = ax3, linewidth = 3, color = 'black', alpha = 1, warn_singular=False)

        #fill tails if specified
        if args.color_tail == True:
            median_boot = statistics.median(bootstraps)
            kde_x, kde_y = ax2.lines[0].get_data()

            if int(observed) < median_boot:
                ax2.fill_between(kde_x, kde_y, where=(kde_x < int(observed)), interpolate=True, color=args.comp_line_color, alpha = 0.75)
            else:
                ax2.fill_between(kde_x, kde_y, where=(kde_x > int(observed)), interpolate=True, color=args.comp_line_color, alpha = 0.75)

        #make plot
        plt.title(f'{mutation}')
        plt.tight_layout()
        pdf = f"{args.outdir}/{mutation}.pdf"
        plt.savefig(pdf)


    #function to make kde plot
    def kde_plot(mutation, observed, bootstraps):

        plt.figure(figsize=(5,5)).tight_layout()
        plt.margins(x=0)
        data = [int(x) for x in bootstraps]

        #default kde plot
        ax = sns.kdeplot(data=data, color = args.plot_color, fill = True)

        if args.color_tail == True:
            median_boot = statistics.median(bootstraps)
            kde_x, kde_y = ax.lines[0].get_data()

            if int(observed) < median_boot:
                ax.fill_between(kde_x, kde_y, where=(kde_x < int(observed)), interpolate=True, color=args.comp_line_color, alpha = 0.75)
            else:
                ax.fill_between(kde_x, kde_y, where=(kde_x > int(observed)), interpolate=True, color=args.comp_line_color, alpha = 0.75)

        #make plot
        plt.title(f'{mutation}')
        plt.tight_layout()
        pdf = f"{args.outdir}/{mutation}.pdf"
        plt.savefig(pdf)
        

    #function to make ecdf plot
    def ecdf_plot(mutation, observed, bootstraps):

        plt.figure(figsize=(5,5)).tight_layout()
        plt.margins(x=0)
        data = [int(x) for x in bootstraps]

        #default ecdf plot
        ax = sns.ecdfplot(data=data)
        plt.axvline(x = observed, color=args.comp_line_color, linewidth = 3)

        #make plot
        plt.title(f'{mutation}')
        plt.tight_layout()
        pdf = f"{args.outdir}/{mutation}.pdf"
        plt.savefig(pdf)

    def make_plot(input):
        #read data file and make plots
        with open(input, 'r') as input:
            lines = input.readlines()
            for line in lines:
                header = bool(re.match('^#', line))
                if header == False:
                    try:
                        bootstraps = line.split('\t')[2].rstrip('\n,').split(',')
                        bootstrap_data = [int(x) for x in bootstraps]
                        mutation = line.split('\t')[0]
                        observed = int(line.split('\t')[1])

                        if args.hist == True:
                            PlotComparisons.histogram_plot(mutation, observed, bootstrap_data)
                        
                        if args.kde == True and args.hist == False:
                            PlotComparisons.kde_plot(mutation, observed, bootstrap_data)
                        
                        if args.ecdf == True:
                            PlotComparisons.ecdf_plot(mutation, observed, bootstrap_data)
                    except:
                        mutation = line.split('\t')[0]
                        print(f'WARNING: No mutations of class {mutation.upper()} found in comparison data.')

PlotComparisons.make_plot(args.input)