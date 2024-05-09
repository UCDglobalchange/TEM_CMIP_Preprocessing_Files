# Scripts to pre-process CMIP5 and CMIP6 Climate Data for the Terrestrial Ecosystem Model (TEM)

This repository provides scripts to process the monthly CMIP5/6 variables in netcdf format: 
- Daily minimum near surface air temperature (tasmin) K
- Daily maximum temperature (tasmax) K
- Near surface air temperature (tas) K
- Near surface specific humidity (huss) Dimensionless
- Surface air pressure (ps) Pa
- Precipitation Flux (pr) kg m-2 s-1
- Surface downwelling shortwave flux in air (rsds) W m-2
- Eastward wind at 10m, u component (uas) m s-1
- Northward wind at 10m, v component (vas) m s-1

More information about these variables (can be found here)[https://pcmdi.llnl.gov/mips/cmip3/variableList.html]  

These CMIP5/6 variables are then turned into the following variables in csv format: 
- Diurnal temperature range (trange) C
- Windspeed at 10m (wind) m s-1
- Vapor Pressure Deficit (vpr) hPa
- Near surface air temperature (tair) C
- Precipitation Flux (precip) mm month-1
- Surface downwelling shortwave flux in air (nirr) W m-2 

Other supporting files:
A csv with the lat / lon / area of the TEM gridcells, here we used the potential vegetation file called cruHurtt3.2.1potmxcohrtsr_hurttlf.glb. This file is added into the repository. Note that this is a global file.

## Description of scripts
Preprocess_CMIP_TEM.py - python script that is submitted to process CMIP variables. currently this script is set up to read in a historical time period and a future time period and process them together. Because this is often not necessary, in the future the script could be modified to take in a single script as opposed to a ds_historical and ds_future.
  
Preprocess_CMIP_TEM.ipynb - jupyter notebook to test code  
 
run_python_script_for_cmip_to_TEM_CMIP6.sh - script that creates a batch job for each variable, model, and scenario
  
submit_python_script_for_cmip_to_TEM.sh - batch job that runs the python file 
  

## How to run these scripts
!!!NOTE CMIP5 FOLDER MIGHT HAVE BUGS ONLY CMIP6 FOLDER IS ACTIVELY MAINTAINED!!! 
1. Download CMIP5/6 Data 
  - There is a script to download CMIP6 (Abigails_PANGEO_CMIP6_Download.ipynb) but does not have all models
  - CMIP5 data can be downloaded from (here)[https://esgf-node.llnl.gov/search/cmip5/]
2. Save all netcdf files in one directory
3. Change the Preprocess*.py script to read in and out of the correct directories
  - read in directory variable "cmip_data_folder"
  - output directory variable "cleaned_data_folder"
  - folder to save diagnostic plots "data_checks_folder"
  - change path to csv with TEM lat/lon/area
4. Open the script run_python_script_for_cmip_to_TEM_CMIP6.sh and confirm all 6 TEM output vars are in the output_vars list
5. Customize submit_python_script_for_cmip_to_TEM.sh as needed for your batch job. Note than ~100GBs are needed to processes the climate data. In the future these scripts can be optimized to run only for the historical time period or only the future timeperiod, since at the end of the script they are broken up.
6. Submit the run python bash script (bash run_python_script_for_cmip_to_TEM_CMIP6.sh), which will submit a bash script for each model, variable, and scenario
