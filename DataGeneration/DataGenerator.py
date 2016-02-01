from DataGeneration import DatabaseHandler
from DataGeneration import MapLocation
from MapboxAPIWrapper import MapboxAPIWrapper


class DataGenerator:

    def __init__(self):
        self.stops = []
        self.handler = DatabaseHandler(full=False)

    def initialize(self):
        self.handler = self.get_database_handler()
        self.stops = self.handler.get_all_stops()

    def begin(self):
        address = self.handler.get_address_without_route()

    def get_database_handler(self, db_file_name='db.sqlite3'):
        handler = DatabaseHandler(db_file_name)
        return handler
