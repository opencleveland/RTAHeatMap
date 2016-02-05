from DataGeneration import DatabaseHandler
from DataGeneration import MapLocation
from MapboxAPIWrapper import MapboxAPIWrapper


class DataGenerator:

    def __init__(self):
        self.stops = []
        self.handler = DatabaseHandler(full=False)
        self.wrapper = MapboxAPIWrapper()

    def initialize(self, db='db.sqlite3', api_key='api_key.txt'):
        self.handler = self.get_database_handler(db)
        self.stops = self.handler.get_all_stops()
        self.wrapper = self.get_api_wrapper(api_key)

    def begin(self):
        address = self.handler.get_address_without_route()

    def get_database_handler(self, db_file_name='db.sqlite3'):
        handler = DatabaseHandler(db_file_name)
        return handler

    def get_api_wrapper(self, api_key_file = 'api_key.txt'):
        wrapper = MapboxAPIWrapper()
        wrapper.load_api_key_from_file(api_key_file)
        return wrapper
