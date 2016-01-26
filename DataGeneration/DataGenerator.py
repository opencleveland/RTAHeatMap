from DatabaseHandler import DatabaseHandler
from MapboxAPIWrapper import MapboxAPIWrapper


class DataGenerator:

    def __init__(self):
        pass

    def start(self):
        handler = self.get_database_handler()

    def get_database_handler(self, db_file_name='db.sqlite3'):
        handler = DatabaseHandler(db_file_name)
        return handler
