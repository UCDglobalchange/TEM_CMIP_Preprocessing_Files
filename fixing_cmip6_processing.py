#!/usr/bin/env python
# coding: utf-8


import xarray as xr
import cftime 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import os
import time
import logging
import cartopy.crs as ccrs
import metpy  # accessor needed to parse crs
import calendar
import argparse



nirr_test = pd.read_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_nirr.csv'
           ,names = ["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name'])

##create dataset to be repeated over all missing years
rep = nirr_test[["lon", 'lat','var' ,'Area', 'Area_Name']].drop_duplicates()

allyrs=np.arange(1500, 2100)
missing_vals = np.isin(allyrs,nirr_test.year.unique())
missing = allyrs[~missing_vals]

for yr in missing:
    df = rep
    df['year']=yr
    nirr_test = pd.concat([nirr_test, df])
    print(yr)

nirr_test=nirr_test.sort_values(by = ['lon', 'lat', 'year'])
nirr_test.interpolate(inplace=True)

nirr_test = nirr_test[["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name']]
nirr_test.to_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_nirr.csv'
            ,float_format='%.3f'
            ,header=False
                 ,index=False
                )


tair_test = pd.read_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_tair.csv'
           ,names = ["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name'])

##create dataset to be repeated over all missing years
rep = tair_test[["lon", 'lat','var' ,'Area', 'Area_Name']].drop_duplicates()

allyrs=np.arange(1500, 2100)
missing_vals = np.isin(allyrs,tair_test.year.unique())
missing = allyrs[~missing_vals]

for yr in missing:
    df = rep
    df['year']=yr
    tair_test = pd.concat([tair_test, df])
    print(yr)

tair_test=tair_test.sort_values(by = ['lon', 'lat', 'year'])
tair_test.interpolate(inplace=True)

tair_test = tair_test[["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name']]
tair_test.to_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_tair.csv'
            ,float_format='%.3f'
            ,header=False
                 ,index=False
                )


prec_test = pd.read_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_prec.csv'
           ,names = ["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name'])

##create dataset to be repeated over all missing years
rep = prec_test[["lon", 'lat','var' ,'Area', 'Area_Name']].drop_duplicates()

allyrs=np.arange(1500, 2100)
missing_vals = np.isin(allyrs,prec_test.year.unique())
missing = allyrs[~missing_vals]

for yr in missing:
    df = rep
    df['year']=yr
    prec_test = pd.concat([prec_test, df])
    print(yr)

prec_test=prec_test.sort_values(by = ['lon', 'lat', 'year'])
prec_test.interpolate(inplace=True)

prec_test = prec_test[["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name']]

prec_test.to_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_prec.csv'
            ,float_format='%.3f'
            ,header=False
                 ,index=False
                )


trange_test = pd.read_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_trange.csv'
           ,names = ["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name'])

##create dataset to be repeated over all missing years
rep = trange_test[["lon", 'lat','var' ,'Area', 'Area_Name']].drop_duplicates()

allyrs=np.arange(1500, 2100)
missing_vals = np.isin(allyrs,trange_test.year.unique())
missing = allyrs[~missing_vals]

for yr in missing:
    df = rep
    df['year']=yr
    trange_test = pd.concat([trange_test, df])
    print(yr)

trange_test=trange_test.sort_values(by = ['lon', 'lat', 'year'])
trange_test.interpolate(inplace=True)

trange_test = trange_test[["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name']]

trange_test.to_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_trange.csv'
            ,float_format='%.3f'
            ,header=False
                 ,index=False
                )


vpr_test = pd.read_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_vpr.csv'
           ,names = ["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name'])

##create dataset to be repeated over all missing years
rep = vpr_test[["lon", 'lat','var' ,'Area', 'Area_Name']].drop_duplicates()

allyrs=np.arange(1500, 2100)
missing_vals = np.isin(allyrs,vpr_test.year.unique())
missing = allyrs[~missing_vals]

for yr in missing:
    df = rep
    df['year']=yr
    vpr_test = pd.concat([vpr_test, df])
    print(yr)

vpr_test=vpr_test.sort_values(by = ['lon', 'lat', 'year'])
vpr_test.interpolate(inplace=True)

vpr_test = vpr_test[["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name']]

vpr_test.to_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_vpr.csv'
            ,float_format='%.3f'
            ,header=False
                 ,index=False
                )

wind_test = pd.read_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_wind.csv'
           ,names = ["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name'])

##create dataset to be repeated over all missing years
rep = wind_test[["lon", 'lat','var' ,'Area', 'Area_Name']].drop_duplicates()

allyrs=np.arange(1500, 2100)
missing_vals = np.isin(allyrs,wind_test.year.unique())
missing = allyrs[~missing_vals]

for yr in missing:
    df = rep
    df['year']=yr
    wind_test = pd.concat([wind_test, df])
    print(yr)

wind_test=wind_test.sort_values(by = ['lon', 'lat', 'year'])
wind_test.interpolate(inplace=True)

wind_test = wind_test[["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name']]

wind_test.to_csv('/home/smmrrr/cleaned_climate_input/CMIP6/CanESM5_ssp245_wind.csv'
            ,float_format='%.3f'
            ,header=False
                 ,index=False
                )





