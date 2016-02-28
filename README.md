# RTAHeatMap

## Purpose
The purpose of this project is to generate walking distance data for a list of address to the nearest public transportation stops and then represent this data as a heatmap.

## Data Generation
The DataGenerator class pulls addresses and stops from an sqlite3 database object, it then inserts generated route data into the same database object. The first step of generating data is to generate this object and populate the address and stops tables of this database.

### Generating the database from scratch
Insantiated a DatabaseHandler object while specifying the file path to the database you wish to create is sufficient to ensure that the database is created and that also has all necessary tables for RTAHeatMap to function.
```python
from RTAHeatMap import *
handler = DatabaseHandler(db='db.sqlite3')
```
### Populating the database
Once we have our database object, we can populate it directly from a .csv file. We need to populate it with both addresses and stops for the DataGenerator to function. We only have to do this once, but you can always add more addresses or stops!
```python
from RTAHeatMap import *
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
from RTAHeatMap import *
generator = DataGenerator()
generator.initialize(db='db.sqlite3', api_key='api_key.txt')
generator.begin()
```
If everything has been setup correctly, you should start to see console output for each address and stop that is processed. It may take some time. The generated data will be added to the routes table of the sqlite database object.

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
