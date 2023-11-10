#!/bin/bash
output_vars=("trange" "wind" "tair" "prec" "nirr" "vpr") #list the variables to be processed
# output_vars=("vpr")
# get list of CMIP6 models and scenarios

runs=$( find /home/smmrrr/TEM_Climate_Data/CMIP6/netcdfs -type f | awk '{ sub(/.*Amon_/, ""); sub(/_r1i1p1f1\.nc/, ""); print $0 }' | awk '$0 !~ /historical/' | sort -u)
echo ${runs[@]}

for run in ${runs[@]}; do
    for output_var in ${output_vars[@]} ; do 
        model=( $(basename $run | cut -d '_' -f 1) )
        scenario=( $(basename $run | cut -d '_' -f 2) )
        # export $scenario
        # export $output_var
        # export $model
        # echo TEM_Climate_Data/read_in_test_CMIP62TEM.py $scenario $model $output_var
        sbatch /home/smmrrr/TEM_Climate_Data/TEM_CMIP_Preprocessing_Files/CMIP6/submit_python_script_for_cmip6_to_TEM.sh $scenario $model $output_var
        done
    done
