#!/bin/bash -l
  
# setting name of job
#SBATCH -J cmip62TEM

# setting home directory
#SBATCH -D /home/smmrrr/

# setting standard error output
#SBATCH -e /home/smmrrr/slurm_log/sterror_%j.txt

# setting standard output
#SBATCH -o /home/smmrrr/slurm_log/stdoutput_%j.txt

# setting medium priority
#SBATCH -p bmh

#SBATCH --nodes=1
#SBATCH --mem=100G
##SBATCH --ntasks=1
###SBATCH --cpus-per-task=1

# setting the max time
#SBATCH -t 10:00:00

# mail alerts at beginning and end of job
##SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END

# send mail here
#SBATCH --mail-user=srauschenbach@ucdavis.edu

scenario=$1
model=$2
output_var=$3

echo TEM_Climate_Data/read_in_test_CMIP62TEM.py $scenario $model $output_var
srun /home/smmrrr/miniconda3/envs/condaforge/bin/python3.10 TEM_Climate_Data/TEM_CMIP_Preprocessing_Files/Preprocess_CMIP6_TEM.py $scenario $model $output_var