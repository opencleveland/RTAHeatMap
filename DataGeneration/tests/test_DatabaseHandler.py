import unittest
from mock import patch, MagicMock, Mock
from DatabaseHandler import DatabaseHandler
from DataGeneration.MapLocation import MapLocation
import os


class TestDatabaseHandler(unittest.TestCase):

    def tearDown(self):
        if os.path.exists('unit_test_db.sqlite3'):
            os.remove('unit_test_db.sqlite3')
        if os.path.exists('test_file.csv'):
            os.remove('test_file.csv')

    # constructor tests
    @patch('DatabaseHandler.sql')
    def test_handler_constructor_connects(self,
                                          mock_sql):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        mock_sql.connect.assert_called_once_with('unit_test_db.sqlite3')

    @patch('DatabaseHandler.sql')
    def test_handler_constructor_default_db_file_name_is_correct(self,
                                                                 mock_sql):
        handler = DatabaseHandler()
        mock_sql.connect.assert_called_once_with('db.sqlite3')

    # construct_db tests
    def test_construct_db_calls_add_address_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        mock_add_addresses = Mock()
        handler._add_addresses_table = mock_add_addresses
        mock_add_stops = Mock()
        handler._add_stops_table = mock_add_stops
        handler.construct_db()
        self.assertTrue(mock_add_addresses.called,
                        "construct_db did not call _add_addresses_table")

    def test_construct_db_calls_add_stop_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        mock_add_addresses = Mock()
        handler._add_addresses_table = mock_add_addresses
        mock_add_stops = Mock()
        handler._add_stops_table = mock_add_stops
        handler.construct_db()
        self.assertTrue(mock_add_stops.called,
                        "construct_db did not call _add_stops_table")

    def test_construct_db_calls_add_route_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        mock_add_addresses = Mock()
        handler._add_addresses_table = mock_add_addresses
        mock_add_stops = Mock()
        handler._add_stops_table = mock_add_stops
        mock_add_routes = Mock()
        handler._add_routes_table = mock_add_routes
        handler.construct_db()
        self.assertTrue(mock_add_routes.called,
                        "construct_db did not call _add_routes_table")

    # table construction tests
    def test_add_addresses_table_adds_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_addresses_table()
        c = handler.conn.cursor()
        c.execute("SELECT NAME FROM sqlite_master WHERE "
                  "TYPE='table' and NAME='addresses'")
        self.assertTrue(c.fetchone(), "addresses table not created")

    def test_add_stops_table_adds_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_stops_table()
        c = handler.conn.cursor()
        c.execute("SELECT NAME FROM sqlite_master WHERE "
                  "TYPE='table' and NAME='stops'")
        self.assertTrue(c.fetchone(), "stops table not created")

    def test_add_routes_table_adds_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_routes_table()
        c = handler.conn.cursor()
        c.execute("SELECT NAME FROM sqlite_master WHERE "
                  "TYPE='table' AND NAME='routes'")
        self.assertTrue(c.fetchone(), "routes table not created")

    # add information to table from file tests
    def test_handler_add_addresses_from_file_inserts_one_record(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        with open('test_file.csv', 'w') as f:
            f.write('latitude,longitude\n')
            f.write('8,12\n')
        handler.add_addresses_from_file('test_file.csv')
        c = handler.conn.cursor()
        c.execute("SELECT latitude, longitude FROM addresses")
        row = c.fetchone()
        self.assertEqual((8, 12), row)

    def test_handler_add_stops_from_file_inserts_one_record(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        with open('test_file.csv', 'w') as f:
            f.write('latitude,longitude\n')
            f.write('15.35,-1.5\n')
        handler.add_stops_from_file('test_file.csv')
        c = handler.conn.cursor()
        c.execute("SELECT latitude, longitude FROM stops")
        row = c.fetchone()
        self.assertEqual((15.35, -1.5), row)

    # add information to tables tests
    def test_add_address_adds_to_address_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_addresses_table()
        handler.add_address(location=MapLocation(latitude=0.56, longitude=9.5))
        c = handler.conn.cursor()
        c.execute("SELECT latitude, longitude FROM addresses")
        row = c.fetchone()
        self.assertEqual((0.56, 9.5), row)

    def test_add_address_errors_if_location_is_not_map_location(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        self.assertRaises(TypeError, handler.add_address, "15")

    def test_add_stop_adds_to_stops_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_stops_table()
        map_location = MapLocation(latitude=-0.55, longitude=80)
        handler.add_stop(location= map_location)
        c = handler.conn.cursor()
        c.execute("SELECT latitude, longitude FROM stops")
        row = c.fetchone()
        self.assertEqual((-.55, 80), row)

    def test_add_stop_errors_if_location_is_not_map_location(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        self.assertRaises(TypeError, handler.add_stop, 13)