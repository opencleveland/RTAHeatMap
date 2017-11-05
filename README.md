# RTAHeatMap

## Purpose
The purpose of this project is to generate walking distance data for a list of address to the nearest public transportation stops and then represent this data as an isochrone map. 


## Set Up 

Our project is currently using python 2.7 

1. Install [pip, virtualenv, and virtualenvwrapper](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md) if you haven't already. 
2. Clone the directory 
3. Go inside the RTAheatmap project folder
4. Create virtualenv for this project ```virtualenv --no-site-packages venv```
5. start your virtualenv by running ```source venv/bin/activate```
6. run ```pip install -r requirements.txt```
7. Sign up for an account at mapbox.com; obtain an API key. create a file named api_key.txt and place the api key in it and save or ask for one in the RTAtracker channel in our slack. 

To create the results, run generate.py. 

Below describes generate.py 


## Data Generation
The DataGenerator class pulls addresses and stops from an sqlite3 database object, it then inserts generated route data into the same database object. The first step of generating data is to generate this object and populate the address and stops tables of this database.

### Generating the database from scratch
Insantiated a DatabaseHandler object while specifying the file path to the database you wish to create is sufficient to ensure that the database is created and that also has all necessary tables for RTAHeatMap to function.

```python
handler = DatabaseHandler(db='db.sqlite3')
```

### Populating the database
Once we have our database object, we can populate it directly from a .csv file. We need to populate it with both addresses and stops for the DataGenerator to function. We only have to do this once, but you can always add more addresses or stops!

```python
handler = DatabaseHandler(db='db.sqlite3')
handler.add_addresses_from_file(file_name='sample_data/sparse_addresses.csv')
handler.add_stops_from_file(file_name='sample_data/sparse_stops.csv')
```

Note: the source .csv files for stops and addresses must have exactly two columns with a header row. The two columns must be titled, "latitude", and "longitude".

### Using a Mapbox API Key
To generate data, we will need a .txt file which contains our API Key. You should name this file "api_key.txt" and save it to the same directory that you will run the Data Generation from (the RTAHeatMap directory is a good place). No need to set anything up at this step besides just making sure this file exists.

### Beginning Analysis
Now you have everything that you need to start generating data. Ensure that your working directory is the same directory that contains the .txt file that contains your API key as well as the database object. Then run the following:

```python
generator = DataGenerator(handler=handler, wrapper=wrapper)
generator.begin()
```

The default location for the database file is 'db.sqlite3' and the default location for the api key is 'api_key.txt' in the same folder that you run the analysis from.
If you'd like to specify an alternative location for the database or the api key file run the following line before generator.begin():

```python
generator.initialize(db='your_db.sqlite3', api_key='my_api_key.txt')
```

If everything has been setup correctly, you should start to see console output for each address and stop that is processed. It may take some time. The generated data will be added to the routes table of the sqlite database object.

The default mode of transportation when DataGenerator.begin() is called is walking. You can also specify driving or cycling by invoking begin with the mode parameter like so:

```python
generator.begin(mode='driving')
# OR
generator.begin(mode='cycling')
```

### Output
Once you have generated data, you can use the following command to output routes to a .csv file:

```python
handler = DatabaseHandler(db='db.sqlite3')
handler.output_routes(file_path='output.csv')
```

Or, to output directly to a dataframe:

```python
import pandas as pd
handler = DatabaseHandler(db='db.sqlite3')
df = handler.routes_dataframe()
# To get a dataframe of only the closest stop for each address:
df = handler.routes_dataframe_closest_stops()
```

## Part 2: The Map

The isochrone map is viewable at http://opencleveland.github.io/RTAHeatMap which displays the time, in minutes, for a person, to walk to the closest RTA transit stop. 

The code for this map is in the gh-pages branch. 


# Details of how to generate the isochrone map

Your output from generate.py is now a CSV file (let's call it theresults.csv) with 3 columns, the `latitude`, `longitude`, and the `walking_time` column (in seconds) that it takes to the closest transit stop. 

First, we need to transform that CSV file into a geojson file. There are numerous ways to do this but in our tutorial, we will use [csv2geojson](https://github.com/mapbox/csv2geojson) and the result geojson file will be theresults.geojson. 

Now, we have a geojson file (theresults.geojson) but `walking_time`'s values are as strings instead of an integer! So, we need to remove the strings (`""`) from the `walking_time`'s values. 

We'll need to do a search for the string `"-?([0-9]+\.?[0-9]+)"` and replace it with `$1`

This turns

```
"properties": {
        "walking_time": "1972.0"
      },
```

into  

```
"properties": {
        "walking_time": 1972.0
      },
```

Now, we need to convert the geojson file of points into isochrone polygons. This is done in QGIS 
using the Contours Plugin. 

# Creating the Contours

Open the geojson file (theresults.geojson) in QGIS. Then open the contours plugin. 

Select `walking_time` as your data field, or an expression if you'd like the walking time in minutes the as shown in the image. 

![Qgis Contour plugin image](https://github.com/opencleveland/RTAHeatMap/blob/master/images/contour-qgis-menu.png)

Select Filled Contours

Also enter the values (your break points) that you wish to create your isochrone bands by.

Run it! 

You have your isochrone file (as a geojson file) to insert into your web map as you wish. 

Our map is one example of inserting it into a web map https://github.com/opencleveland/RTAHeatMap/tree/gh-pages

## Contributing

To contribute to this project:

1. Fork this repo
2. Make a feature branch for your addition
3. Make your changes
4. If implementing new functionality, include new tests
5. Commit your changes to that branch
6. Run all tests to make sure everything still passes
7. Push the change to your fork
8. Make a pull Request to this Repo and we'll merge your changes in


If you have questions about the project or need help setting it up, Open an issue or 
email opencleveland@gmail.com 
