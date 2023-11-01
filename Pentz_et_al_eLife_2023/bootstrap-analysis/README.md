# Descriptions of primary scripts and/or implementation instructions

### bootstrap-mutation-frequencies.py
Usage: \
./bootstrap-mutation-frequencies.py \
-i input_annotations.csv \
-c comparison_annotations.csv \
-b number_of_bootstraps \
-o output_file_handle \
-p 

Description: \
-i, --input    A list of categorical mutation annotations in .csv format with no header line, required \
-c, --comparison    A list of categorical mutation annotations in .csv format with no header line for the input to be assessed against, required \
-b, --bootstraps    The number of bootstrap replicates (i.e., the number of times the comparison imput will be subsampled for comparison to the input, required \
-o, --output    Handle that will be added to all produced output files (necessary extensions will be added), required \
-p, --plot    Plot histograms showing the distribution of bootstrap runs and were the input falls in this distribution, optional \

Notes: \
To run this script, the Pandas python package must be installed. \
To produce plots, the Matplotlib and Seaborn python packages but be installed. 
