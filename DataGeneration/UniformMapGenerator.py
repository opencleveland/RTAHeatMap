# The purpose of this class is to generate a uniformly distributed series of
#  lat/long coordinates given max/min latitude, max/min longitude, latitude
#  resolution, and longitude resolution, where resolution is the desired number
#  of degrees between output coordinates
# Outputs a pandas dataframe of lat/long coordinate pairs

import pandas as pd    # For the dataframe
import numpy as np     # To calculate ranges with float step-values
import math            # For math


class UniformMapGenerator:

    def __init__(self):
        pass

    def GetUniformCoordinateMap(self,
                                lat_min,
                                lat_max,
                                lng_min,
                                lng_max,
                                lat_res,
                                lng_res):

        latitude_num = self.get_number_of_intervals(lat_min, lat_max, lat_res)
        longitude_num = self.get_number_of_intervals(lng_min, lng_max, lng_res)
        total_coordinate_rows = latitude_num * longitude_num

        # Output some data for debugging
        print('Latitude Quantity: ' + str(latitude_num))
        print('Longitude Quantity: ' + str(longitude_num))
        print('Total Number of Rows to Output: ' + str(total_coordinate_rows))

        output_df = self.instantiate_output_dataframe(total_coordinate_rows)

        # Iterate through each latitude and each longitude calculated with the
        # np.arange function, adding lat_res to the max value to ensure that we
        # include the max value in the range that we iterate through
        row_num = 0
        for lat in np.arange(lat_min, lat_max + lat_res, lat_res):
            for lng in np.arange(lng_min, lng_max + lng_res, lng_res):
                output_df.loc[row_num] = [lat, lng] #Add the lat/lng pair to the dataframe
                row_num += 1 #increment our row number
        return output_df

    # Returns the number of intervals (int) between minimum and maximum that
    # include the minimum and maximum where each interval is 'resolution'
    # distance apart
    def get_number_of_intervals(self, minimum, maximum, resolution):
        return int(math.ceil((maximum - minimum) / resolution + 1))

    def instantiate_output_dataframe(self, total_rows):
        return pd.DataFrame(columns = ['addr_lat','addr_lon'],
                            index = range(0, total_rows))


# Example UniformMapGenerator Usage
#  The example below will accept Latitude/Longitude parameters and output
#  uniform coordinates to a file called my_uniform_coordinates.csv
#
# These values are the degrees walked per minute at a speed of 3.1 miles per
# hour at 41.4822 deg N and 81.6697 deg W, which is the center of Cleveland
#LATITUDE_RESOLUTION = 0.000724516
#LONGITUDE_RESOLUTION = 0.000963461
#LATITUDE_MINIMUM = 41.227883
#LATITUDE_MAXIMUM = 41.637051
#LONGITUDE_MINIMUM = -81.96753
#LONGITUDE_MAXIMUM = -81.438542
#
#output_df = UniformMapGenerator.GetUniformCoordinateMap(LATITUDE_MINIMUM,
#                                                        LATITUDE_MAXIMUM,
#                                                        LONGITUDE_MINIMUM,
#                                                        LONGITUDE_MAXIMUM,
#                                                        LATITUDE_RESOLUTION,
#                                                        LONGITUDE_RESOLUTION)
#
#output_df.to_csv('my_uniform_coordinates.csv')
