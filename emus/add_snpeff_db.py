#!/usr/bin/env python3

import os
import argparse
import re

#get command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('-o', '--organism', metavar = '<Organism ID>', 
    help = "Organism name as genus_species")
parser.add_argument('-i', '--db_id', metavar = '<Database name>', 
    help = "Name to identify database for variant annotaiton")
parser.add_argument('-g', '--genome', metavar='<Genome file>', 
    help = "FASTA file containing genome sequence")
parser.add_argument('-f', '--features', metavar = '<Features file>', 
    help = "Gene features file in GTF format")
parser.add_argument('-n', '--note', 
    help = 'Comment to help identify database in config file when manually searching')

#arguments to find and get pre-built databases
parser.add_argument('-s', '--search', default = '', metavar = '<Database ID>',
    help = "Find pre-built database: format search input as 'genus_species'")
parser.add_argument('-d', '--download_db', default = '', metavar = 'Database ID', 
    help = "Database ID to download from SnpEff")
args = parser.parse_args()

class MakeSnpEffdb:
    def __init__(self, genome, features):
        self.genome = genome
        self.features = features
    
    #function to locate snpeff config file
    def check_snpeff():
        #locate snpeff bin by looking for its symlink
        snpeff_exe = os.popen('which snpeff').read().rstrip()
        snpeff_path = os.popen(f'ls -lia {snpeff_exe}').read().rstrip().split()
        snpeff_bin = snpeff_path[9].split('/')[1:-1]
        snpeff_bin_path = ''
        for dir in snpeff_bin:
            snpeff_bin_path = snpeff_bin_path + f'/{dir.rstrip()}'

        #locate path to main dir by tracing back simlink
        snpeff_link = snpeff_path[-1].split('/')[0:-1]
        snpeff_main_path = ''
        for dir in snpeff_link:
            snpeff_main_path = snpeff_main_path + f'/{dir}'
        path_to_main_snpeff = snpeff_bin_path + snpeff_main_path

        #locate config file
        config = os.popen(f'ls {path_to_main_snpeff}/snpeff.config').read().rstrip()
        if config == f'{path_to_main_snpeff}/snpeff.config':
            print(f'snpeff.config found at: {path_to_main_snpeff}/snpeff.config')
        else:
            print('snpeff.config file was not found')
        
        #locate data directory
        search = os.popen(f'ls {path_to_main_snpeff}').readlines()
        if 'data\n' not in search:
            print('data directory not found')
            os.system(f'mkdir {path_to_main_snpeff}/data')
            print(f'data directory added at: {path_to_main_snpeff}/data')
        else:
            print('data directory located')
        return path_to_main_snpeff

    def add_database(snpeff_location):
        #make database directory and move files
        os.system(f'mkdir {snpeff_location}/data/{args.db_id}')
        os.system(f'cp {args.genome} {snpeff_location}/data/{args.db_id}/sequences.fa')
        os.system(f'cp {args.features} {snpeff_location}/data/{args.db_id}/genes.gtf')
        
        #edit config file
        with open(f'{snpeff_location}/snpeff.config', 'a') as config:
            config.write(f'\n')
            config.write(f'# {args.note}\n')
            config.write(f'{args.db_id}.genome : {args.organism}')
            config.close()
        
        #build database
        os.system(f'snpeff build -v {args.db_id}')
        
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


#search for database
if len(args.find) != 0:
    MakeSnpEffdb.find_databases(args.find)
    exit()

if len(args.download_db) != 0:
    MakeSnpEffdb.download_database(args.download_db)
    exit()
    
#locate snpeff main directory
snpeff_location = MakeSnpEffdb.check_snpeff()

#add database
MakeSnpEffdb.add_database(snpeff_location)