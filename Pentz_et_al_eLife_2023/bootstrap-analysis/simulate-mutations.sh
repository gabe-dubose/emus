#!/bin/bash

#To implement Mutation-Simulator, I created a conda environment to install dependencies
#This was done according to the guidelines on https://github.com/mkpython3/Mutation-Simulator
#To run this script, Mutation-Simulator must be installed in a conda environment called "mutation-simulator"
#This can be done form within the script as well

help=0
make=0
while getopts "g:p:v:o:x:mh" option
do
    case $option in 
        g) genome=$OPTARG;;
        p) SNP=$OPTARG;;
        o) output=$OPTARG;;
        x) path=$OPTARG;;
        m) make=1;;
        h) help=1;;
    esac
done

if [ $help -eq 1 ]; then
    echo "Generate random mutations across a gene or genome
    This script wraps the Mutation-Simulator mutation-simulator.py script to
    generate random mutations across an input genome in FASTA format. 
    *Note: please make sure you have your mutation-simulator conda environment active
    Usage:
    -g [input genome in FASTA format]
    -p [number of SNPs to be generates] *note: this number is transitioned into a frequency by
       dividing the the number you provide by the lenght of the genome
    -o [output file handle]
    -x [path to Matation-Simulator directory] *(if already set-up)
    -m use flag to set up Mutation-Simulator 
       *note: conda and git must be installed on machine
    -h view help options
    Note: the conda environment 'mutation simulator' must be activated"
    exit 1
fi

if [ $make -eq 1 ]; then
    echo "Path to download Mutation-Simulator:"
    read path_ms
    cd $path_ms
    git clone https://github.com/mkpython3/Mutation-Simulator
    echo "Mutation-Simulator repository cloned from https://github.com/mkpython3/Mutation-Simulator"
    cd Mutation-Simulator
    conda env create --file environment.yml
    echo "conda environment created"
    chmod u+x mutation-simulator.py
    echo "Setup complete"
    exit 1
fi


#Calculate mutation frequency by dividing user input number of SNPs divided by length of genome
genome_length=$(egrep -o "^[ATCGatcg]" ${genome} | wc -l)
echo "Genome Length: ${genome_length}"
declare -i s=${SNP}
#subtraction it to adjust for variability induced by float limitations, may need to be manually adjusted if used in the future
declare -i l=${genome_length}-100392
echo "Adjustment: ${l}"
snp_freq=$(awk -v a=$s -v b=$l -v OFMT=%.100g 'BEGIN{print a / b}' | bc -l)
echo "SNP Frequency: ${snp_freq}"

#run Mutation-Simulator
cd ${path}
./mutation-simulator.py \
${genome} \
args -sn ${snp_freq}
