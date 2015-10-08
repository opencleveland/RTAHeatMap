# The objective of this script is to generate a dataset that is the closest
# 20 stops for a list of addresses. The stops are public transportation stops,
# and the addresses are randomly distributed addresses throughout a city.
# The end goal of this dataset is to produce a heat map reflecting the
# accessibility of public transportation throughout the city.

import math           #To do math
import pandas as pd   #To store our datasets
import dbfread as dbf #To read our .dbf file
import csv            #To write to .csv
import googlemaps

ClientKey = 'AIzaSyAb3C7URjaEjSh59C8UfbM576bWJHWYMTw'
gmaps = googlemaps.Client(key = ClientKey)
 
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

# Method to Run the top n_stops for each address into the Google API, and 
# output only the closest of the 5 stops.
def return_closest_stop_via_gmaps(stop_df):
    #TODO: Utilize Batching so we don't hit the server for every row    
    
    lowestvalue = 9999999
    for i, add in stop_df.iterrows():
        origin = {'lat': add['addr_lat'], 'lng': add['stop_lon']}
        dest= {'lat': add['stop_lat'], 'lng': add['stop_lon']}        
        dist = gmaps.distance_matrix(origins = origin, 
                             destinations = dest, 
                             mode='walking')
        dist2 = dist['rows'][0]['elements'][0]
        thisvalue = dist2['duration']['value']
        if (thisvalue < lowestvalue) and (thisvalue != 0):
            lowestvalue = thisvalue
            outputrow = [thisvalue, 
                         dist2['duration']['text'],
                         dist2['distance']['text'],
                         add['stop_lat'], add['stop_lon'], 
                         add['addr_lat'], add['addr_lon'],
                         add['sl_dist']]
    #Sort our outputrow array on the first element (dist2['duration']['value'])
    #Return the top element, which will be the lowest duration value
    #print(outputrow)
    return(outputrow)

# Method to calculate and save the closest n_stops Stops for each address to 
# an output .csv file
def get_closest_stops_for_each_address(addresses, stops, n_stops):
    columns = ['stop_lat','stop_lon','addr_lat','addr_lon','sl_dist']
    df = pd.DataFrame(columns = ['distvalue', 'duration','distance'] + columns)     
    for i, addr in addresses.iterrows():
        stop_df = pd.DataFrame(columns = columns)
        for j, stop in stops.iterrows():
            dist = distance_on_unit_sphere(stop['stop_lat'], stop['stop_lon'], 
                                           addr['addr_lat'], addr['addr_lon'])
            stop_df.loc[j] = [stop['stop_lat'], stop['stop_lon'], 
                              addr['addr_lat'], addr['addr_lon'], dist]
        #Sort the DataFrame, Add the n_stops entries with lowest distance to df
        stop_df = stop_df.sort('sl_dist')
        stop_df = stop_df.head(n_stops)
        
        #Feed our potential address-stop matches to the google API
        #and append the resulting row to the final DataFrame we will return.
        newrow = return_closest_stop_via_gmaps(stop_df)
        df = df.append(newrow)               
    return df

finaldf = get_closest_stops_for_each_address(get_addresses(), get_stops(), 5)
finaldf.to_csv("output.csv")