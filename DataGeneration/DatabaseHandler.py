import sqlite3 as sql
import pandas as pd
from DataGeneration.MapLocation import MapLocation


class DatabaseHandler:

    def __init__(self, db_file_name='db.sqlite3'):
        self.conn = sql.connect(db_file_name)

    def construct_db(self):
        self._add_addresses_table()
        self._add_stops_table()
        self._add_routes_table()

    def _add_addresses_table(self):
        c = self.conn.cursor()
        c.execute("""
                  CREATE TABLE IF NOT EXISTS addresses
                  (id INTEGER PRIMARY KEY,
                  latitude real NOT NULL,
                  longitude real NOT NULL)
                  """)

    def _add_stops_table(self):
        c = self.conn.cursor()
        c.execute("""
                  CREATE TABLE IF NOT EXISTS stops
                  (id INTEGER PRIMARY KEY,
                  latitude real NOT NULL,
                  longitude real NOT NULL)
                  """)

    def _add_routes_table(self):
        c = self.conn.cursor()
        c.execute("""
                  CREATE TABLE IF NOT EXISTS routes
                  (id INTEGER PRIMARY KEY,
                  address_id INTEGER NOT NULL,
                  stop_id INTEGER NOT NULL,
                  distance INTEGER NOT NULL,
                  time INTEGER NOT NULL,
                  FOREIGN KEY(address_id) REFERENCES addresses(id),
                  FOREIGN KEY(stop_id) REFERENCES stops(id))
                  """)

    def add_addresses_from_file(self, file_name):
        df = pd.read_csv(file_name)
        df.to_sql('addresses', self.conn, if_exists='append', index=False)

    def add_stops_from_file(self, file_name):
        df = pd.read_csv(file_name)
        df.to_sql('stops', self.conn, if_exists='append', index=False)

    def add_address(self, location):
        if not isinstance(location, MapLocation):
            raise TypeError('location must be of type MapLocation')
        c = self.conn.cursor()
        c.execute("INSERT INTO addresses (latitude, longitude)"
                  "VALUES (?, ?)", (location.latitude, location.longitude))

    def add_stop(self, location):
        if not isinstance(location, MapLocation):
            raise TypeError('location must be of type MapLocation')
        c = self.conn.cursor()
        c.execute("INSERT INTO stops (latitude, longitude)"
                  "VALUES (?, ?)", (location.latitude, location.longitude))
