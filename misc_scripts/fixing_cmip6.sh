#!/bin/bash -l

# setting name of job
#SBATCH -J fix_clim_input

# setting standard error output
#SBATCH -e slurm_out_%j

# setting standard output
#SBATCH -o slurm_out_%j

# setting medium priority
#SBATCH -p high2

# Request ! CPUs and 128 GB of RAM from 1 node:
#SBATCH --nodes=1
#SBATCH --mem=100G
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1

# setting the max time
#SBATCH -t 24:00:00

# mail alerts at beginning and end of job
#SBATCH --mail-type=FAIL
#SBATCH --mail-type=END

# send mail here
#SBATCH --mail-user=srauschenbach@ucdavis.edu

# run one thread for each one the user asks the queue for
# hostname is just for debugging

cd ${SLURM_SUBMIT_DIR}
srun fixing_cmip6_processing.py