#!/usr/bin/env python
# coding: utf-8

# In[1]:


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


# In[2]:


##parse command line arguments

parser = argparse.ArgumentParser()
parser.add_argument("scenario", help = '')
parser.add_argument("model", help = '')
parser.add_argument("output_var", help = '')
args = parser.parse_args()


# In[75]:


##create a lookup table that matches TEM var names to CMIP
##this is only for variables without any var transformation

TEM2CMIP_varnames = np.array([['tair', 'prec', 'rsds'],
['tas' ,'pr', 'nirr']])



# In[77]:


##use this when working with jupyter labs as it does not take command line args
#scenario = 'rcp45'
#model = 'GFDL-CM3'
#output_var = 'tair'
scenario = args.scenario
model = args.model
output_var = args.output_var


# In[78]:


#### READ IN CLIMATE DATA
#there is different logic for each variable
#variable transformations done before formatting into TEM


folder1 = 'TEM_Climate_Data/' #folder where climate data is 
# folder2 = 'TEM__preprocess_examples' #folder for testing the script

   
if (args.output_var == 'trange'): #subtract max and min temp

    ds_historical_max = xr.open_dataset('~/'+folder1+'tasmax_'+scenario+'/'+model+'_concat.nc')
    ds_future_max = xr.open_dataset('~/'+folder1+'tasmax_historical/'+model+'_concat.nc')
    ds_historical_min = xr.open_dataset('~/'+folder1+'tasmin_'+scenario+'/'+model+'_concat.nc')
    ds_future_min = xr.open_dataset('~/'+folder1+'tasmin_historical/'+model+'_concat.nc')

    ds_max = ds_historical_max.combine_first(ds_future_max)
    ds_min = ds_historical_min.combine_first(ds_future_min)

    ds = xr.merge([ds_max
                   , ds_min])

    ds['var_of_interest'] = ds['tasmax'] -  ds['tasmin']
    ds = ds.drop_vars(['tasmin', 'tasmax'])    

elif (output_var == 'wind'): #calc the ws using the u and v vectors
    
    ds_historical_uas = xr.open_dataset('~/'+folder1+'uas_'+scenario+'/'+model+'_concat.nc')
    ds_future_uas = xr.open_dataset('~/'+folder1+'uas_historical/'+model+'_concat.nc')
    ds_historical_vas = xr.open_dataset('~/'+folder1+'vas_'+scenario+'/'+model+'_concat.nc')
    ds_future_vas = xr.open_dataset('~/'+folder1+'vas_historical/'+model+'_concat.nc')

    ds_uas = ds_historical_uas.combine_first(ds_future_uas)
    ds_vas = ds_historical_vas.combine_first(ds_future_vas)

    ds = xr.merge([ds_uas
                   , ds_vas])

    ds['var_of_interest'] = np.sqrt(ds['uas']**2 +  ds['vas']**2)
    

else:
    output_var_lookup = np.where(TEM2CMIP_varnames == output_var)[1] ##look up location of tem var 
    output_var_match = TEM2CMIP_varnames[1, output_var_lookup] ##get cmip var
    cmip_var = re.sub('[\[\]\']', '', np.array_str(output_var_match)) #clean format of cmip var

    ds_historical = xr.open_dataset('~/'+folder1+cmip_var+'_'+scenario+'/'+model+'_concat.nc')
    ds_future = xr.open_dataset('~/'+folder1+cmip_var+'_historical/'+model+'_concat.nc')
    ds = ds_historical.combine_first(ds_future)

    ds['var_of_interest'] = ds[cmip_var]
    ds = ds.drop_vars([cmip_var])

    
### OLD FOR TESTING

# ds_historical = xr.open_dataset('~/'+folder2+'/'+'tas_Amon_ACCESS1-0_historical_r1i1p1_185001-200512.nc')
# ds_future = xr.open_dataset('~/'+folder2+'/'+'tas_Amon_ACCESS1-0_rcp85_r1i1p1_200601-210012.nc')
# ds = ds_historical.combine_first(ds_future)

## the tem file that has the correct lat/lon 
TEM = pd.read_csv('~/TEM__preprocess_examples/igsmtbaselv0.5x0.5degree.glb'
                 ,names = [ 'lon', 'lat', 'Variable', 'Area', 'Elev','Area_Name'])


print('read in')
# In[14]:


# ds = xr.concat([ds_historical, ds_future], dim = 'y')


#### SWITCH COORDS ON CLIMATE DATA
#Convert longitude coordinates from 0-359 to -180-179
ds = ds.assign_coords(lon=(((ds.lon + 180) % 360) - 180))
# move lat / lon up .25 degrees to account for center vs. corner of grid cell


ds = ds.sortby('lon')

ds = ds.drop_dims('bnds')

ds = ds.drop_vars('height')

if(len(ds.data_vars) > 1):
    tt = re.compile(r'^(?!var_of_interest$).*$')
    var_to_remove = [i for i in ds.data_vars if tt.match(i)]
    ds = ds.drop_vars(var_to_remove) 


#ds.plot.scatter(x = 'lon', y = 'lat') #, hue = 'Area_Name')
#TEM.plot.scatter(x = 'lon', y = 'lat') #, hue = 'Area_Name')


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

monthly = xr.merge([ds.isel(time=(ds.time.dt.month == n)).rename(
            {'var_of_interest': calendar.month_abbr[n] }) for n in range(1, 13)])

monthly = monthly.groupby(ds.time.dt.year).min()

# tt.groupby(ds.time.dt.year).max() ##check they are the same

print('monthly transform')



final = xr.merge([voi_stats, 
                      monthly
         ])
final

print('stats merged')


#### DO THE NEAREST LON/LAT 

##old method
# TEM = TEM.set_index(['lon', 'lat'])
# TEM_xr = TEM.to_xarray()

#new method 
# TEM = TEM.reset_index()
TEM_xr = TEM.set_index(['lon', 'lat'])
TEM_xr = TEM_xr[['Area', 'Area_Name']].to_xarray()
print('tem to xarray')
TEM_xr = TEM_xr.assign_coords(lon=(TEM_xr.lon + 0.25))
TEM_xr = TEM_xr.assign_coords(lat=(TEM_xr.lat + 0.25))
print('assign tem coords')

ds_TEM = final.reindex_like(TEM_xr, method = 'nearest')
#ds_TEM

print('reindex done')
# In[89]:


# TEM_xr.sel(lon = -180, lat = -16.5)
# ds_TEM.sel(lon = -180, year = 1960)


# In[90]:


#verify that the nearest lon/lat is working 
# final.sel(lat = -55.25, lon = -180.25, year = 1960).to_pandas()
# ds_TEM.sel(lat = -55.5, lon = -180, year = 1960).to_pandas()



# In[25]:


##take a look at bounds of lat/lon in final vs ds_TEM
print(final['lon'])
# print(ds_TEM['lon'])

print(final['lat'])
# print(ds_TEM['lat']) ## !!!is the -0.25 right on the edge cases of -90 and 90?!!!


# In[26]:


## TEM is higher resolution than the climate data
# 3012*720*280 #months x lon x lat 
# 3012*192*145 #months x lon x lat 
#83854080 #number of rows in climate dataset
#607219200 #number of rows in matched dataset 
print(ds_TEM.Jan.count())
print(final.Jan.count())


# In[ ]:


#### FORMAT USING OLD SCRIPT 

#get list of variable names
#do the correct transformation by variable name 


# In[290]:


# list(range(10, 310, 10))


# In[27]:


for i in range(10, 310, 10):

    rep_decade = ds_TEM.sel(year = slice(1850, 1859))
    rep_decade['year'] = rep_decade.year - i

    if i == 10:
        rep_past = rep_decade
    else:
        rep_past = rep_past.combine_first(rep_decade)

    print(i)
    
    
rep_past


# In[30]:


ds_TEM = ds_TEM.combine_first(rep_past)

print(ds_TEM.year.min())
print(ds_TEM.year.max())


# In[31]:


ds_TEM = xr.merge([ds_TEM, TEM_xr])


# In[ ]:


ds_TEM2 = ds_TEM.to_dataframe()

ds_TEM2.count()
# In[21]:


ds_TEM2 = ds_TEM2.dropna()


# In[22]:


ds_TEM2 = ds_TEM2.reset_index()


# In[23]:


print(ds_TEM2['lat'].nunique())
print(ds_TEM2['lon'].nunique())
print(ds_TEM2['year'].nunique())


# In[24]:


# 280*720*551
cvar = 'temp'


# In[25]:


ds_TEM2['var'] = ' ' + cvar + ' '


ds_TEM2 = ds_TEM2[["lon", 'lat','var' ,'Area', 'year', 'sum', 'max', 'average'
         , 'min', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct'
         , 'Nov', 'Dec', 'Area_Name']]



# In[ ]:


ds_TEM2.to_csv('~/TEM_Monthly/cleaned_climate_input/'+model+'_'+scenario+'_'+output_var+'.csv',index = False)


# In[26]:


# ds

## get coordinates 
systime = time.ctime(time.time())
print(f"\nStart time: {systime}")


# In[ ]:


###### old program that is too slow replicated from R program TEM_historical_kelley_chu.R


# i = 1
# year = 1888


# lon = round(TEM.loc[i, 'lon'], 4)
# lat = round(TEM.loc[i, 'lat'], 4)
    
# if (lat < 0 or lon < 0):  ##is this what we want?? lat is 
#                     #always negative so this isnt doing anything
#     lat = lat + 90
#     lon = lon + 180
            
# lat = lat + 0.25
# lon = lon + 0.25
        
# if year < 1861:
#     year_l = str(year)
#     year_l = year_l[-1]
#     year_l = 1860 + int(year_l)
# else: 
#     year_l = year
    
# t_index = np.min(np.where(ds['time'].dt.year == year_l))
# t_index = t_index +  [i for i in range(12)]
# lon_index = np.argmin(np.array(np.abs(ds['lon'] - lon)))
# lat_index = np.argmin(np.array(np.abs(ds['lat'] - lat)))
# ds_subset = ds.isel(time=t_index, lat = [lat_index], lon = [lon_index])
# ds_subset = ds_subset.to_dataframe()
# ds_subset = ds_subset.reset_index()
# ds_subset['sum_val'] = ds_subset['tas'].sum()
# ds_subset['min_val'] = ds_subset['tas'].min()
# ds_subset['max_val'] = ds_subset['tas'].max()
# ds_subset['avg_val'] = ds_subset['tas'].mean()
# ds_subset['var'] = TEM.loc[i, 'Variable']
# ds_subset['area'] = TEM.loc[i, 'Area']
# ds_subset['year'] = year
# ds_subset['lat_TEM'] = lat
# ds_subset['lon_TEM'] = lon

