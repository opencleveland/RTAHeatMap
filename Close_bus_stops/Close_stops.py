
import pandas as pd


def datafame_of_close_stops(given_lat, given_lon, df, given_range=0.005):
    selectedDf = df[(df.stop_lat > (given_lat - given_range)) \
                    & (df.stop_lat < (given_lat + given_range))\
                    &(df.stop_lon > (given_lon - given_range)) \
                    & (df.stop_lon < (given_lon + given_range))]
    return selectedDf


def main():

    stopCSVfileName = "/Users/TakuyaSakaguchi/Jupyter_Python3/stops.csv"
    df = pd.read_csv(stopCSVfileName)

    lat = 41.392864
    lon = -81.536557

    selectedStopsDf = datafame_of_close_stops(lat, lon, df)

    print(selectedStopsDf.head())
    print("\n")
    print(len(selectedStopsDf))

if __name__ == "__main__":
    main()
