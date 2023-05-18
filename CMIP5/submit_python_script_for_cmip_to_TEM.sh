#!/bin/bash -l
  
# setting name of job
#SBATCH -J bcc-csm1

# setting home directory
#SBATCH -D /home/smmrrr/

# setting standard error output
#SBATCH -e /home/smmrrr/slurm_log/sterror_%j.txt

# setting standard output
#SBATCH -o /home/smmrrr/slurm_log/stdoutput_%j.txt

# setting medium priority
#SBATCH -p high2

#SBATCH --mem=1G

# setting the max time
#SBATCH -t 10:00:00

# mail alerts at beginning and end of job
##SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END

# send mail here
#SBATCH --mail-user=srauschenbach@ucdavis.edu



srun /home/smmrrr/miniconda3/envs/condaforge/bin/python3.10 TEM_Climate_Data/Preprocess_TEM.py $scenario $model $output_var
