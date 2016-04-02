# RTAHeatMap

## Purpose
The purpose of this project is to generate walking distance data for a list of address to the nearest public transportation stops and then represent this data as a heatmap.

## Data Generation
The DataGenerator class pulls addresses and stops from an sqlite3 database object, it then inserts generated route data into the same database object. The first step of generating data is to generate this object and populate the address and stops tables of this database.

To use this package use the following import statement (assuming this directory is in your python path):
```python
from RTAHeatMap import *
```
### Generating the database from scratch
Insantiated a DatabaseHandler object while specifying the file path to the database you wish to create is sufficient to ensure that the database is created and that also has all necessary tables for RTAHeatMap to function.
```python
handler = DatabaseHandler(db='db.sqlite3')
```
### Populating the database
Once we have our database object, we can populate it directly from a .csv file. We need to populate it with both addresses and stops for the DataGenerator to function. We only have to do this once, but you can always add more addresses or stops!
```python
handler = DatabaseHandler(db='db.sqlite3')
handler.add_addresses_from_file(file_name='stops.csv')
handler.add_stops_from_file(file_name='addresses.csv')
```
Note: the source .csv files for stops and addresses must have exactly two columns with a header row. The two columns must be titled, "latitude", and "longitude".

### Using a Mapbox API Key
To generate data, we will need a .txt file which contains our API Key. You should name this file "api_key.txt" and save it to the same directory that you will run the Data Generation from (the RTAHeatMap directory is a good place). No need to set anything up at this step besides just making sure this file exists.

### Beginning Analysis
Now you have everything that you need to start generating data. Ensure that your working directory is the same directory that contains the .txt file that contains your API key as well as the database object. Then simply run the following:
```python
generator = DataGenerator()
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

## HeatMap Generation
This portion of the project is still in its infancy, please feel free to contribute!

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
