#!/usr/bin/env python
# -*- coding: utf-8 -*-

from DataGeneration.MapboxAPIWrapper import MapboxAPIWrapper
from DataGeneration.DatabaseHandler import DatabaseHandler
from DataGeneration.DataGenerator import DataGenerator
from overhead.constants import api_key_file_path

# I modified this from the instructions
handler = DatabaseHandler('db.sqlite3')

handler.add_addresses_from_file(file_name='sample_data/sparse_addresses.csv')
handler.add_stops_from_file(file_name='sample_data/sparse_stops.csv') 

wrapper = MapboxAPIWrapper()
wrapper.load_api_key_from_file(api_key_file_path)
generator = DataGenerator(handler=handler, wrapper=wrapper)
generator.begin()
# generator.initialize(db='db.sqlite3', api_key='api_key.txt')
handler.output_routes(file_path='output.csv')