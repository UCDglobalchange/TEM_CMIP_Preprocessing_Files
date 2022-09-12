#!/bin/bash

scenarios=("rcp45" "rcp85" "rcp60") #list the scenarios used

output_vars=("trange" "wind" "tair" "prec") #list the variables to be processed

# get list of models that have been successfully concatenated 
models=( $( find . -type f  | grep '.*concat.nc$' | awk '{ sub(/\.\/.*\//, ""); sub(/_concat\.nc/, ""); print $0 }' | sort -u) )
echo ${model[@]}

for scenario in ${scenarios[@]}; do
    for output_var in ${output_vars[@]} ; do
        for model in ${models[@]} ; do
        export scenario=$scenario
        export output_var=$output_var
        export model=$model
        echo srun /home/smmrrr/miniconda3/envs/condaforge/bin/python3.10 TEM_Climate_Data/Preprocess_TEM.py $scenario $model $output_var
        # sbatch ~/TEM_Climate_Data/submit_python_script_for_cmip_to_TEM.sh 
        done
    done
done
