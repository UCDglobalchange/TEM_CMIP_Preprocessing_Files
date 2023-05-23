#!/usr/bin/env python
# coding: utf-8

## read in packages
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

def custom_cftime(x): ##input CMIP6 dataset which has the column named 'time'
    units, reference_date = x.time.attrs['units'].split(' since ') #get units and starting time
    timedelta = pd.to_timedelta(x.time, unit = units)
    x['time'] = pd.to_datetime(reference_date) + timedelta #reassigned these values to the time coordinate
    print(units, reference_date) ##optional, used for debugging

systime = time.ctime(time.time())
print(f"\nStart time: {systime}")

##parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("scenario", help = '')
parser.add_argument("model", help = '')
parser.add_argument("output_var", help = '')
args = parser.parse_args()

##define directories
cmip_data_folder = '/home/smmrrr/TEM_Climate_Data/CMIP6/' #folder where climate data is 
data_checks_folder = '/home/smmrrr/TEM_Climate_Data/TEM_CMIP_Preprocessing_Files/Datachecks/'
cleaned_data_folder = '/home/smmrrr/cleaned_climate_input/CMIP6/'

##create a lookup table that matches TEM var names to CMIP
##this is only for variables without any var transformation
TEM2CMIP_varnames = np.array([['tair', 'prec', 'nirr'],
['tas' ,'pr', 'rsds']])


##use this when working with jupyter labs as it does not take command line args
#scenario = 'rcp45'
#model = 'GFDL-CM3'
#output_var = 'tair'

#assign args to text values
scenario = args.scenario
model = args.model
output_var = args.output_var


#### READ IN CLIMATE DATA
#there is different logic for each variable
#variable transformations done before formatting for TEM


   
if (output_var == 'trange'): #subtract max and min temp
# folder + variable + '_Amon_' + model + '_' + scenario + '_r1i1p1f1.nc' 
    ds_historical_max = xr.open_dataset(cmip_data_folder+'tasmax' + '_Amon_' + model + '_historical_r1i1p1f1.nc' , decode_times=False)
    custom_cftime(ds_historical_max)
    ds_future_max = xr.open_dataset(cmip_data_folder +'tasmax' + '_Amon_' + model + '_' + scenario + '_r1i1p1f1.nc' , decode_times=False)
    custom_cftime(ds_future_max)
    ds_historical_min = xr.open_dataset(cmip_data_folder+'tasmin' + '_Amon_' + model + '_historical_r1i1p1f1.nc' , decode_times=False)
    custom_cftime(ds_historical_min)
    ds_future_min = xr.open_dataset(cmip_data_folder+ 'tasmin' + '_Amon_' + model + '_' + scenario + '_r1i1p1f1.nc' , decode_times=False)
    custom_cftime(ds_future_min)

    ds_max = ds_historical_max.combine_first(ds_future_max)
    ds_min = ds_historical_min.combine_first(ds_future_min)

    ds = xr.merge([ds_max
                   , ds_min])

    ds['var_of_interest'] = ds['tasmax'] -  ds['tasmin']
    ds = ds.drop_vars(['tasmin', 'tasmax'])    

elif (output_var == 'wind'): #calc the ws using the u and v vectors
    
    ds_historical_uas = xr.open_dataset(cmip_data_folder+'uas' + '_Amon_' + model + '_historical_r1i1p1f1.nc', decode_times=False)
    custom_cftime(ds_historical_uas)
    ds_future_uas = xr.open_dataset(cmip_data_folder + 'uas' + '_Amon_' + model + '_' + scenario + '_r1i1p1f1.nc' , decode_times=False)
    custom_cftime(ds_future_uas)
    ds_historical_vas = xr.open_dataset(cmip_data_folder + 'vas' + '_Amon_' + model + '_historical_r1i1p1f1.nc' , decode_times=False)
    custom_cftime(ds_historical_vas)
    ds_future_vas = xr.open_dataset(cmip_data_folder + 'vas' + '_Amon_' + model + '_' + scenario + '_r1i1p1f1.nc' , decode_times=False)
    custom_cftime(ds_future_vas)

    ds_uas = ds_historical_uas.combine_first(ds_future_uas)
    ds_vas = ds_historical_vas.combine_first(ds_future_vas)

    ds = xr.merge([ds_uas
                   , ds_vas])

    ds['var_of_interest'] = np.sqrt(ds['uas']**2 +  ds['vas']**2)
    
elif (output_var == 'vpr'): #calc the vapor pressure using specific humidity and surface pressure
    
    ds_historical_huss = xr.open_dataset(cmip_data_folder+ 'huss'+ '_Amon_' + model + '_historical_r1i1p1f1.nc', decode_times=False)
    custom_cftime(ds_historical_huss)
    ds_future_huss = xr.open_dataset(cmip_data_folder+ 'huss' + '_Amon_' + model + '_' + scenario + '_r1i1p1f1.nc' , decode_times=False)
    custom_cftime(ds_future_huss)
    ds_historical_ps = xr.open_dataset(cmip_data_folder+ 'ps'+ '_Amon_' + model + '_historical_r1i1p1f1.nc', decode_times=False)
    custom_cftime(ds_historical_ps)
    ds_future_ps = xr.open_dataset(cmip_data_folder+ 'ps' + '_Amon_' + model + '_' + scenario + '_r1i1p1f1.nc' , decode_times=False)
    custom_cftime(ds_future_ps)

    ds_huss = ds_historical_huss.combine_first(ds_future_huss)

    ds_ps = ds_historical_ps.combine_first(ds_future_ps)

    ds = xr.merge([ds_huss
                     , ds_ps])


    ds['var_of_interest'] = (ds['huss']*ds['ps'])/(0.622 + 0.378*ds['huss'])
    ##using this equation for vapor pressure e = (qp)/(0.622 + 0.378q)
    #where q is specific humidity in kg/kg and p is atmospheric pressure in pa
    #https://cran.r-project.org/web/packages/humidity/vignettes/humidity-measures.html
    # ds['var_of_interest'] = ds[cmip_var]
    # ds = ds.drop_vars([cmip_var])


else:
    output_var_lookup = np.where(TEM2CMIP_varnames == output_var)[1] ##look up location of tem var 
    output_var_match = TEM2CMIP_varnames[1, output_var_lookup] ##get cmip var
    cmip_var = re.sub('[\[\]\']', '', np.array_str(output_var_match)) #clean format of cmip var

    ds_historical = xr.open_dataset(cmip_data_folder+ cmip_var + '_Amon_' + model + '_historical_r1i1p1f1.nc' , decode_times=False)
    custom_cftime(ds_historical)
    ds_future = xr.open_dataset(cmip_data_folder+ cmip_var + '_Amon_' + model + '_' + scenario + '_r1i1p1f1.nc' , decode_times=False)
    custom_cftime(ds_future)
    ds = ds_historical.combine_first(ds_future)

    ds['var_of_interest'] = ds[cmip_var]
    ds = ds.drop_vars([cmip_var])


## the tem file that has the lat/lon we are regridding to
TEM = pd.read_csv(
    '/home/smmrrr/TEM_Climate_Data/LULCC/support_files/cruHurtt3.2.1potmxcohrtsr_hurttlf.glb'
     ,names = [ 'lon', 'lat', 'file', 'Area', 'num1','num2','num3', 'Area_Name'])
# ds['var_of_interest'] = ds['tas']

# ds_uas ## used for troubleshooting different lat / lon coords for access cm2
TEM = TEM[[ 'lon', 'lat','Area' ,'Area_Name']]

print('read in')


#### SWITCH COORDS ON CLIMATE DATA
#Convert longitude coordinates from 0-359 to -180-179
ds = ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180))
# move lat / lon up .25 degrees to account for center vs. corner of grid cell


ds = ds.sortby('lon')

ds = ds.drop_dims('bnds')

# ds = ds.drop_vars('height')


##some files have different variables so we are dropping them
if(len(ds.data_vars) > 1):
    tt = re.compile(r'^(?!var_of_interest$).*$')
    var_to_remove = [i for i in ds.data_vars if tt.match(i)]
    print(var_to_remove)
    ds = ds.drop_vars(var_to_remove) 
###are some of these differences in height?

#ds.plot.scatter(x = 'lon', y = 'lat') #, hue = 'Area_Name')
#TEM.plot.scatter(x = 'lon', y = 'lat') #, hue = 'Area_Name')


##GET SUMMARY STATS
##voi stands for variable of interest
voi_mean = ds.groupby(ds.time.dt.year).mean()
voi_min = ds.groupby(ds.time.dt.year).min()
voi_max = ds.groupby(ds.time.dt.year).max()
voi_sum = ds.groupby(ds.time.dt.year).sum()


voi_stats = xr.merge([voi_sum.rename({'var_of_interest':'sum'}), 
                      voi_max.rename({'var_of_interest':'max'}),
                    voi_mean.rename({'var_of_interest':'average'}),
                      voi_min.rename({'var_of_interest':'min'})
                     ])
voi_stats


print('stats collected')

##transform data to have a col for each month
monthly = xr.merge([ds.isel(time=(ds.time.dt.month == n)).rename(
            {'var_of_interest': calendar.month_abbr[n] }) for n in range(1, 13)])

monthly = monthly.groupby(ds.time.dt.year).min()

# tt.groupby(ds.time.dt.year).max() ##check they are the same

print('monthly transform')


##merge on annual stats
final = xr.merge([voi_stats, 
                      monthly
         ])
final

print('stats merged')


#### DO THE NEAREST LON/LAT 

##get tem into xarray
TEM_xr = TEM.set_index(['lon', 'lat'])
TEM_xr = TEM_xr[['Area', 'Area_Name']].to_xarray()
print('tem to xarray')
##change to find center of grid
TEM_xr = TEM_xr.assign_coords(lon=(TEM_xr.lon + 0.25))
TEM_xr = TEM_xr.assign_coords(lat=(TEM_xr.lat + 0.25))
print('assign tem coords')

ds_TEM = final.reindex_like(TEM_xr, method = 'nearest')

print('reindex done')



# TEM_xr.sel(lon = -180, lat = -16.5)
# ds_TEM.sel(lon = -180, year = 1960)


#verify that the nearest lon/lat is working 
# final.sel(lat = -55.25, lon = -180.25, year = 1960).to_pandas()
# ds_TEM.sel(lat = -55.5, lon = -180, year = 1960).to_pandas()

##take a look at bounds of lat/lon in final vs ds_TEM
#print(final['lon'])
# print(ds_TEM['lon'])

#print(final['lat'])
# print(ds_TEM['lat']) ## !!!is the -0.25 right on the edge cases of -90 and 90?!!!

##### plot original and tem regridded time period average
fig, axs = plt.subplots(nrows=2, figsize = (9, 9))
plot1 = ds_TEM.mean(dim = ['year']).average.plot(ax = axs[0], cbar_kwargs={'label': 'Average '+output_var})
plot2 = final.mean(dim = ['year']).average.sel( 
    lat = slice(int(ds_TEM.lat.min()), int(ds_TEM.lat.max()))).plot(ax = axs[1], cbar_kwargs={'label': 'Average '+output_var})
# cbar1 = plt.colorbar(plot1, ax=axs[0])
# plot2.cbar.set_label(label = 'Average '+output_var, size = 12)
plt.tight_layout()
plt.savefig(data_checks_folder+'plots/lat_lon_average_'+model+'_'+output_var+'.pdf')

####get average of all lat / lons over time
orig_coords = final.mean(dim = ['lat', 'lon']).average.to_dataframe().reset_index()
tem_coords = ds_TEM.mean(dim = ['lat', 'lon']).average.to_dataframe().reset_index()
orig_coords = orig_coords.rename(columns={'average':'orig_average'})
tem_coords = tem_coords.rename(columns={'average':'tem_average'})
year_compare = orig_coords.merge(tem_coords)
year_compare['model'] = model
year_compare['output_var'] = output_var
year_compare.to_csv(data_checks_folder+'time_average_'+model+'_'+output_var+'.csv')

## TEM is higher resolution than the climate data
# 3012*720*280 #months x lon x lat 
# 3012*192*145 #months x lon x lat 
#83854080 #number of rows in climate dataset
#607219200 #number of rows in matched dataset 
#print(ds_TEM.Jan.count())
#print(final.Jan.count())


####generate data from 1550, repeating the 10 decades of variability from 1850 to 1859
for i in range(10, 310, 10):

    rep_decade = ds_TEM.sel(year = slice(1850, 1859))
    rep_decade['year'] = rep_decade.year - i

    if i == 10:
        rep_past = rep_decade
    else:
        rep_past = rep_past.combine_first(rep_decade)

    print(i)
       
#rep_past

##merge on repeated past data
ds_TEM = ds_TEM.combine_first(rep_past)

# print(ds_TEM.year.min())
# print(ds_TEM.year.max())

##merge to TEM to get the area of each grid cell
ds_TEM = xr.merge([ds_TEM, TEM_xr])

##convert to pandas
ds_TEM2 = ds_TEM.to_dataframe()

# ds_TEM2.count()

##drop nas and reindex
ds_TEM2 = ds_TEM2.dropna()
ds_TEM2 = ds_TEM2.reset_index()

# print(ds_TEM2['lat'].nunique())
# print(ds_TEM2['lon'].nunique())
# print(ds_TEM2['year'].nunique())

##assign var to be output variable
ds_TEM2['var'] = ' ' + output_var + ' '

##name columns as TEM likes it
ds_TEM2 = ds_TEM2[["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name']]


##save as a csv
ds_TEM2.to_csv(cleaned_data_folder+model+'_'+scenario+'_'+output_var+'.csv',index = False)



systime = time.ctime(time.time())
print(f"\nEnd time: {systime}")

