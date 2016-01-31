

'''
Requirements:
pandas
geopy
'''

import pandas as pd
from geopy.distance import vincenty


def dataframe_of_close_stops(given_lat, given_lon, df, given_range=0.007225):
    selectedDf = df[(df.stop_lat > (given_lat - given_range)) \
                    & (df.stop_lat < (given_lat + given_range))\
                    &(df.stop_lon > (given_lon - given_range)) \
                    & (df.stop_lon < (given_lon + given_range))]
    return selectedDf


def get_number_of_close_stops(given_lat, given_lon, df, given_range=0.007225):
    number = len(dataframe_of_close_stops(given_lat, given_lon, df, given_range))
    return number


def Add_distance_to_dataframe(addr_df, destination_lat, destination_lon):
    addr_df.index = range(0, len(addr_df))
    for i in range(len(addr_df)):
        addr_df.loc[i, "distance"] = vincenty((destination_lat, destination_lon), \
                                              (addr_df.loc[i, "stop_lat"], addr_df.loc[i,"stop_lon"])).miles
    return addr_df


def main():

    stopCSVfileName = "/Users/TakuyaSakaguchi/Jupyter_Python3/stops.csv"
    stop_df = pd.read_csv(stopCSVfileName)

    lat = 41.592864
    lon = -81.536557

    selectedStopsDf = dataframe_of_close_stops(lat, lon, stop_df)



    print(selectedStopsDf.head())
    print("\n")
    print(get_number_of_close_stops(lat, lon, stop_df))

if __name__ == "__main__":
    main()
