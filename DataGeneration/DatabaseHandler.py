import sqlite3 as sql
import csv
import pandas as pd


class DatabaseHandler:

    def __init__(self, db_file_name='db.sqlite3'):
        self.conn = sql.connect(db_file_name)
        self.db_cursor = self.conn.cursor()
        self._create_location_table_if_not_exists('Source')
        self._create_location_table_if_not_exists('TransitStop')

    def _create_location_table_if_not_exists(self, table_name):
        self.db_cursor.execute("create table if not exists {} "
                               "(latitude real, longitude real)".
                               format(table_name))

    def add_rows_from_csv(self, file_name, table_name):
        df = pd.read_csv(file_name)
        df.to_sql(table_name, self.conn, if_exists='append', index=False)


