#!/bin/bash

scenarios=("rcp45" "rcp85" "rcp60") #list the scenarios used

output_vars=("vpr", "trange", "wind", "tair", "prec") #list the variables to be processed

# get list of models that have been successfully concatenated 
models=( $( find . -type f  | grep '.*concat.nc$' | awk '{ sub(/\.\/.*\//, ""); sub(/_concat\.nc/, ""); print $0 }' | sort -u) )
echo ${model[@]}

for scenario in ${scenarios[@]}; do
    for output_var in ${output_vars[@]} ; do
        for model in ${models[@]} ; do
        export $scenario
        export $output_var
        export $model
        sbatch ~/TEM_Climate_Data/submit_python_script_for_cmip_to_TEM.sh
        done
    done
