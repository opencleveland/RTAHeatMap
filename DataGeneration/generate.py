# The objective of this script is to generate a dataset that is the closest
# 20 stops for a list of addresses. The stops are public transportation stops,
# and the addresses are randomly distributed addresses throughout a city.
# The end goal of this dataset is to produce a heat map reflecting the
# accessibility of public transportation throughout the city.

import math  # To do math
import pandas as pd  # To store and manipulate our datasets
import googlemaps  # To do our API calls
import time  # To sleep if the API call fails

ClientKey = '<Insert API Key>'
gmaps = googlemaps.Client(key=ClientKey)


# Method for calculating distance
def distance_on_unit_sphere(lat1, long1, lat2, long2):
    # Source: http://www.johndcook.com/blog/python_longitude_latitude/

    # Convert latitude and longitude to spherical coordinates in radians.
    degrees_to_radians = math.pi / 180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * degrees_to_radians
    phi2 = (90.0 - lat2) * degrees_to_radians

    # theta = longitude
    theta1 = long1 * degrees_to_radians
    theta2 = long2 * degrees_to_radians

    # Compute spherical distance from spherical coordinates.
    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
           math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cos)

    radius_of_earth = 6371  # kilometers
    return arc * radius_of_earth


# Load stops into a pandas dataframe
def get_stops():
    return pd.read_csv("stops.csv")


# Load addresses into a pandas dataframe
def get_addresses():
    return pd.read_csv("sparse_addresses.csv")


# Returns the google API output of the two locations or dummy data if it fails
# to get valid data too many times. It will sleep 10 seconds if it doesn't get
# valid input and then try again. 
def single_gmaps_output(addr_lat, addr_lon, stop_lat, stop_lon,
                        sl_dist, wait=10, threshold=10):
    done = False
    times_run = 0
    while not done:
        try:
            dist = gmaps.distance_matrix(origins={'lat': addr_lat,
                                                  'lng': addr_lon},
                                         destinations={'lat': stop_lat,
                                                       'lng': stop_lon},
                                         mode='walking')
            # If we've failed more than the threshold paramter number of times
            # then return dummy data
            if times_run > threshold: # failed too many times, return dummy data
                return [-1, -1, -1, -1, sl_dist,
                        addr_lat, addr_lon, '',
                        stop_lat, stop_lon, '', times_run]
            # Check to see if we got an elements status of Zero Results
            # If we did: wait, then try again
            if dist['rows'][0]['elements'][0]['status'] == 'ZERO_RESULTS':
                print('No results. Trying again in ' + str(wait) + ' seconds')
                time.sleep(wait)
                times_run += 1
                continue
            a = dist['rows'][0]['elements'][0]['distance']['text']
            d = float(a[:a.find("km") - 1])
            # Check to see if we got absurd data. We will say it is absurd if
            # the distance we calculated in a straight-line is more than 10
            # times what google told us the walking distance was.
            if d < sl_dist / 10:
                print('Received absurd data. Trying again in 10 seconds...')
                time.sleep(wait)
                times_run += 1
                continue
            done = True  # We got a valid and reasonable value if we got here!
        except:
            print('Error Getting our Data. Trying again in 10 seconds...')
            time.sleep(wait)
            times_run += 1
            continue
        # Return what we got back!
        dist2 = dist['rows'][0]['elements'][0]
        outputrow = [dist2['duration']['value'],
                     dist2['duration']['text'],
                     dist2['distance']['value'],
                     dist2['distance']['text'],
                     sl_dist,
                     addr_lat,
                     addr_lon,
                     dist['origin_addresses'][0],
                     stop_lat,
                     stop_lon,
                     dist['destination_addresses'][0],
                     times_run + 1]
        return outputrow


# Method to calculate and save the closest n_stops Stops for each address to
# an output .csv file. It will also query the google API to produce walking
# data.
def get_closest_stops_for_each_address(addresses, stops, n_stops):
    gl_index = 0
    pair_columns = ['stop_lat', 'stop_lon', 'addr_lat', 'addr_lon', 'sl_dist']
    pair_api_columns = ['duration_value', 'duration',
                        'distance_value', 'distance',
                        'straight_line_distance',
                        'addr_lat', 'addr_lon', 'addr_address',
                        'stop_lat', 'stop_lon', 'stop_address',
                        'total_api_calls', 'address_num',
                        'closest']
    output_df = pd.DataFrame(columns=pair_api_columns)
    for i, addr in addresses.iterrows():
        print('address ' + str(i) + ': ' + str(addr))
        # This will store our addr-stop pairs with straight-line distance
        pair_df = pd.DataFrame(columns=pair_columns)

        for j, stop in stops.iterrows():
            dist = distance_on_unit_sphere(stop['stop_lat'], stop['stop_lon'],
                                           addr['addr_lat'], addr['addr_lon'])
            pair_df.loc[j] = [stop['stop_lat'], stop['stop_lon'],
                              addr['addr_lat'], addr['addr_lon'], dist]
            # Sort the DataFrame, Add n_stops entries with lowest distance to df
        pair_df = pair_df.sort('sl_dist')
        pair_df = pair_df.head(n_stops)
        # This will store our subsets of n_stops stops for each address.
        # Once used it to determine which stop is closest, we will add every
        # row that it contains to output_df
        pair_api_df = pd.DataFrame(columns=pair_api_columns)

        # Feed our address-stop pairs to the google API to get the walking
        # distance and time between them.
        for j, pair in pair_df.iterrows():
            newrow = single_gmaps_output(pair['addr_lat'], pair['addr_lon'],
                                         pair['stop_lat'], pair['stop_lon'],
                                         pair['sl_dist'], 10, 10)
            try:
                pair_api_df.loc[gl_index] = (newrow + [i, False])
            except ValueError:
                # Sometimes newrow is only 13 cols when it needs to be 14.
                # don't know why. This just adds another value to the array.
                # A better solution may just be to make a one-row dataframe,
                # that way we can append, and pandas will automatically
                # match the columns up.
                print('Value Error!')
                pair_api_df.loc[gl_index] = (newrow + [i, False, False])
            gl_index += 1
        # Assign True to the 'closest' column of the address-stop pair that
        # has the minimum walking distance for this address
        min_distance_index = pair_api_df['distance_value'].idxmin()
        pair_api_df.ix[min_distance_index,'closest'] = True
        output_df = output_df.append(pair_api_df)
    return output_df

finaldf = get_closest_stops_for_each_address(get_addresses(), get_stops(), 5)
finaldf.to_csv("output.csv")
