#!/bin/bash -l
  
# setting name of job
#SBATCH -J cmip2TEM_format

# setting home directory
#SBATCH -D /home/smmrrr/TEM_Climate_Data

##SBATCH -e /home/smmrrr/slurm_log/sterror_%j.txt 
##SBATCH -o /home/smmrrr/slurm_log/stdoutput_%j.txt

# setting medium priority
#SBATCH -p high2

#SBATCH --mem=12G

# setting the max time
#SBATCH -t 10:00:00

# mail alerts at beginning and end of job
#SBATCH --mail-type=BEGIN
#SBATCH --mail-type=END

# send mail here
#SBATCH --mail-user=srauschenbach@ucdavis.edu



srun ~/TEM_Climate_Data/Process_Data_for_TEM.py $future $historical $cvar
