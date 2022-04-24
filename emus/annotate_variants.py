#!/usr/bin/env python3

import os
import argparse
import re

#get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i', '--input', metavar = '<VCF File>',
    help = "Variant call file to be annotated")
parser.add_argument('-r', '--reference', metavar = '<Reference Database>', 
    help = 'Genome databse to be used in variant annotaiton')
parser.add_argument('-o', '--output', metavar = '<Output handle>', 
    help = "Handle for outputfile")

parser.add_argument('-f', '--find', default = '', metavar = '<Database ID>',
    help = "Find pre-built database: format search input as 'genus_species'")
parser.add_argument('-d', '--download_db', default = '', metavar = 'Database ID', 
    help = "Database ID to download from SnpEff")
args = parser.parse_args()

#Class to annotate variants
class AnnotateVariants:
    def __init__(self, vcf, genome):
        self.vcf = vcf
        self.genome = genome

    #function to search for pre-built snpeff database
    def find_databases(term):
        databases = os.popen('snpeff databases').readlines()
        for db in databases:
            found = bool(re.match(term, db))
            if found == True:
                db = db.split()
                db_id = db[0]
                db_loc = db[2]
                print(f'{db_id}\t{db_loc}')

    #function to download pre-built snpeff database
    def download_database(id):
        os.system(f'snpeff download {id}')

    #function to get variant annotations
    def get_variant_annotations():
        print('Annotating Variants...')
        os.system(f'snpeff eff {args.reference} {args.input} > {args.output}')
     
#search for database
if len(args.find) != 0:
    AnnotateVariants.find_databases(args.find)
    exit()

#downlaod database
if len(args.download_db) != 0:
    AnnotateVariants.download_database(args.download_db)
    exit()

#annotate variants
AnnotateVariants.get_variant_annotations()

