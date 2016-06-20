#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DataGeneration.MapboxAPIWrapper import MapboxAPIWrapper
from DataGeneration.DatabaseHandler import DatabaseHandler
from DataGeneration.UniformMapGenerator import UniformMapGenerator
from DataGeneration.MapLocation import MapLocation
from DataGeneration.DataGenerator import DataGenerator

# I modified this from the instructions
handler = DatabaseHandler('db.sqlite3')

handler.add_addresses_from_file(file_name='sparse_addresses.csv')
handler.add_stops_from_file(file_name='sparse_stops.csv') 

generator = DataGenerator()
generator.begin()
generator.initialize(db='db.sqlite3', api_key='my_api_key.txt')