from DataGeneration import DatabaseHandler
from DataGeneration import MapLocation
from MapboxAPIWrapper import MapboxAPIWrapper


class DataGenerator:

    def __init__(self):
        self.stops = []

    def initialize(self):
        handler = self.get_database_handler()
        self.stops = handler.get_all_stops()

    def get_database_handler(self, db_file_name='db.sqlite3'):
        handler = DatabaseHandler(db_file_name)
        return handler
