# The objective of this script is to generate a dataset that is the closest
# 20 stops for a list of addresses. The stops are public transportation stops,
# and the addresses are randomly distributed addresses throughout a city.
# The end goal of this dataset is to produce a heat map reflecting the
# accessibility of public transportation throughout the city.

import math           #To do math
import pandas as pd   #To store our datasets
import dbfread as dbf #To read our .dbf file
import csv            #To write to .csv
 
# Method for calculating distance
def distance_on_unit_sphere(lat1, long1, lat2, long2):
	#Source: http://www.johndcook.com/blog/python_longitude_latitude/
	
    # Convert latitude and longitude to spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
	
    radius_of_earth = 3959 #Miles
    return arc * radius_of_earth
	
# Load stops into a pandas dataframe
def get_stops():
    return pd.read_csv("stops.csv")

# Convert addresses.dbf file to csv
def convert_addresses_to_csv():
    with open('addresses.csv', 'wb') as csvfile:
        headerexists = False
        for rec in dbf.DBF('LBRS_Site.dbf'):
            if headerexists == False:
                writer = csv.DictWriter(csvfile, fieldnames=rec.keys())
                writer.writeheader()
                headerexists = True
            writer.writerow(rec)

# Load addresses into a pandas dataframe
def get_addresses():
    return pd.read_csv("sparse_addresses.csv")

# Method to calculate and save the closest n_stops Stops for each address to 
# an output .csv file
def get_closest_stops_for_each_address(addresses, stops, n_stops):
    columns = ['stop_lat','stop_lon','addr_lat','addr_lon','distance']
    df = pd.DataFrame(columns = columns)     
    for i, addr in addresses.iterrows():
        stop_df = pd.DataFrame(columns = columns)
        for j, stop in stops.iterrows():
            dist = distance_on_unit_sphere(stop['stop_lat'], stop['stop_lon'], 
                                           addr['addr_lat'], addr['addr_lon'])
            stop_df.loc[j] = [stop['stop_lat'], stop['stop_lon'], 
                              addr['addr_lat'], addr['addr_lon'], dist]
        #Sort the DataFrame, Add the n_stops entries with lowest distance to df
        stop_df = stop_df.sort('distance')
        stop_df = stop_df.head(n_stops)
        
        #Append what we've found to our DataFrame we will Return
        df = df.append(stop_df)                
    return df

finaldf = get_closest_stops_for_each_address(get_addresses(), get_stops(), 5)
finaldf.to_csv("output.csv")

# Method to Run the top n_stops for each address into the Google API, and 
# output only the closest of the 5 stops.
# TODO: Implement
