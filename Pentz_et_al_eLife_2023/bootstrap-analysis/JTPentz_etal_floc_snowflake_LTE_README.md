# Statistically Comparing Mutation Frequencies in Snowflake and Flocculating Yeasts to Randomly Simulated Mutations

## Approach
To evaluate whether different types of mutations are occurring at higher frequencies than randomly expected, we first simulate 100,000 random mutations in the reference genome. This is done to generate a null expectation of how random mutations present. We then call these mutations, and randomly select the number of mutations we found in the study from this null distribution. These frequencies are then compared to the frequencies of the mutations observed in the experiment. This same resampling process was performed 1000 times to see what portion of the time we saw differences between the two treatments that is at least as large as the one we saw experimentally. 

## Implementation

### Simulation of random mutations in reference genome
The Saccharomyces cerevisiae strain S288C reference genome (R64-2-1) (RefSeq: GCF_000146045.2) was used for mutation simulations, consistent with the reference used in the experiment.
The simulate-mutations.sh script (found in this directory) was the ran as:

./simulate-mutations.sh \
-g GCF_000146045.2_R64_genomic.fna \
-p 100000 \
-x Mutation-Simulator \
-o scerv_S288C

### Annotation of simulated variants
Simulated mutations were then annotated using SnpEff, consistent with the experiment. The tool was implemented as follows:

java -jar snpEff.jar build -gtf22 -noCheckCds -noCheckProtein -v S_cerv_288c
java -jar snpEff.jar S_cerv_288c GCF_000146045.2_R64_genomic_ms.vcf > S_cerv_annot.vcf

### Comparing yeat mutation frequencies to simulation
Finally, annotatated variants were extracted and used in the bootstrap-mutation-frequencies.py script (found in this directory):

Comparing Flocs to simulation \
./compare-mutation-frequencies.py \
-i Floc_mutations.csv \
-c Random_mutations.csv \
-b 1000 \
-o Flocs_vs_Simulated \
-p

Comparing Snowflakes to simulation \
./compare-mutation-frequencies.py \
-i Snowflake_mutations.csv \
-c Random_mutations.csv \
-b 1000 \
-o Snowflakes_vs_Simulated \
-p

Note: Mutation lists will be posted after publication
