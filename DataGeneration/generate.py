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
	
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
         
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
	
	#Units Assume radius of 1 . Units Irrelevant as we're only comparing.
    return arc 
	
# Method to Load in all Descriptions-Latitude-Longitudes from stops.csv
	# Perhaps a pandas dataframe?
def get_stops():
    return pd.read_csv("stops.csv")

# Method to Convert or .dbf file to csv
def convert_addresses_to_csv():
    with open('addresses.csv', 'wb') as csvfile:
        headerexists = False
        for rec in dbf.DBF('LBRS_Site.dbf'):
            if headerexists == False:
                writer = csv.DictWriter(csvfile, fieldnames=rec.keys())
                writer.writeheader()
                headerexists = True
            writer.writerow(rec)

# Method to Load in all Addresses from the Cuyahoga

# Method to Save the closest 20 Stops for each Address to an 
# output .csv or JSON (whichever is better for the google API)


# Method to loop through every address
	# and every stop
		# and feed the top 20 closest stops to the Save method above

#for stop in get_stops().iterrows():
    #print(stop)