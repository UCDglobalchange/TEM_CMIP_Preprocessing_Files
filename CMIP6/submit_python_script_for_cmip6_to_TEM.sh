#!/bin/bash -l
  
# setting name of job
#SBATCH -J cmip62TEM

# setting standard error output
#SBATCH -e out/out_%j.txt

# setting standard output
#SBATCH -o out/out_%j.txt

# setting medium priority
#SBATCH -p high2

#SBATCH --nodes=1
#SBATCH --mem=100G
##SBATCH --ntasks=1
###SBATCH --cpus-per-task=1

# setting the max time
#SBATCH -t 10:00:00

# mail alerts at beginning and end of job
##SBATCH --mail-type=BEGIN
#SBATCH --mail-type=FAIL

# send mail here
#SBATCH --mail-user=srauschenbach@ucdavis.edu

scenario=$1
model=$2
output_var=$3

echo $scenario $model $output_var
srun /home/smmrrr/miniconda3/envs/condaforge/bin/python3.10 /home/smmrrr/TEM_Climate_Data/TEM_CMIP_Preprocessing_Files/CMIP6/historical_split.py $scenario $model $output_var
# srun /home/smmrrr/miniconda3/envs/condaforge/bin/python3.10 TEM_Climate_Data/TEM_CMIP_Preprocessing_Files/CMIP6/Preprocess_CMIP6_TEM.py $scenario $model $output_var
