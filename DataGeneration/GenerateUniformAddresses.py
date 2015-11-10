# The purpose of this script is to generate a uniformly distributed series of
#  lat/long coordinates given max/min latitude, max/min longitude, latitude
#  resolution, and longitude resolution, where resolution is the desired number
#  of degrees between output coordinates
# Outputs a pandas dataframe of lat/long coordinate pairs

import pandas as pd    # For the dataframe
import numpy as np     # To calculate ranges with float step-values
import math            # For math

# These values are the degrees walked per minute at a speed of 3.1 miles per
# hour at 41.4822 deg N and 81.6697 deg W, which is the center of Cleveland
LATITUDE_RESOLUTION = 0.000724516
LONGITUDE_RESOLUTION = 0.000963461
LATITUDE_MINIMUM = 41.227883
LATITUDE_MAXIMUM = 41.637051
LONGITUDE_MINIMUM = -81.96753
LONGITUDE_MAXIMUM = -81.438542

def GenerateUniformCoordinates(lat_min,
                               lat_max,
                               lng_min,
                               lng_max,
                               lat_res,
                               lng_res):
                                 
  # Calculate the number of rows our output DataFrame will contain so that we
  # can pre-allocate the memory for the dataframe using the index property.
  nrows_lat = math.ceil((lat_max - lat_min) / lat_res + 1)
  nrows_lng = math.ceil((lng_max - lng_min) / lng_res + 1)
  nrows = nrows_lat * nrows_lng
  
  # Output some data for debugging
  print('Latitude Quantity: ' + str(nrows_lat))
  print('Longitude Quantity: ' + str(nrows_lng))
  print('Total Number of Rows to Output: ' + str(nrows))  
  
  # Instantiate or DataFrame
  df = pd.DataFrame(columns = ['lat','lng'], index=np.arange(0, nrows))
  
  # Iterate through each latitude and each longitude calculated with the
  # np.arange function, adding lat_res to the max value to ensure that we
  # include the max value in the range that we iterate through
  row_num = 0
  for lat in np.arange(lat_min, lat_max + lat_res, lat_res):
    for lng in np.arange(lng_min, lng_max + lng_res, lng_res):
      df.loc[row_num] = [lat, lng] #Add the lat/lng pair to the dataframe
      row_num += 1 #increment our row number
  return df

output_df = GenerateUniformCoordinates(LATITUDE_MINIMUM,
                                       LATITUDE_MAXIMUM,
                                       LONGITUDE_MINIMUM,
                                       LONGITUDE_MAXIMUM,
                                       LATITUDE_RESOLUTION,
                                       LONGITUDE_RESOLUTION)
output_df.to_csv('uniform_addresses.csv')