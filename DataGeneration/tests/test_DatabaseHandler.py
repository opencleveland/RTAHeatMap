import unittest
from mock import patch, MagicMock, Mock
from DatabaseHandler import DatabaseHandler
from DataGeneration.MapLocation import MapLocation
import os
import types
import pandas as pd


class TestDatabaseHandler(unittest.TestCase):

    def setUp(self):
        if os.path.exists('unit_test_db.sqlite3'):
            os.remove('unit_test_db.sqlite3')
        if os.path.exists('test_file.csv'):
            os.remove('test_file.csv')

    def tearDown(self):
        if os.path.exists('unit_test_db.sqlite3'):
            os.remove('unit_test_db.sqlite3')
        if os.path.exists('test_file.csv'):
            os.remove('test_file.csv')

    # constructor tests
    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    @patch('DatabaseHandler.sql')
    def test_handler_constructor_connects(self,
                                          mock_sql,
                                          mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        mock_sql.connect.assert_called_once_with('unit_test_db.sqlite3')

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    @patch('DatabaseHandler.sql')
    def test_handler_constructor_uses_correct_default_db(self,
                                                         mock_sql,
                                                         mock_init_db):
        handler = DatabaseHandler()
        mock_sql.connect.assert_called_once_with('db.sqlite3')

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    @patch('DatabaseHandler.sql')
    def test_handler_constructor_calls_initialize_db(self,
                                                     mock_sql,
                                                     mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        mock_init_db.assert_called_once_with()

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    @patch('DatabaseHandler.sql')
    def test_handler_constructor_doesnt_connect_if_full_is_false(self,
                                                                 mock_sql,
                                                                 mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3', full=False)
        self.assertFalse(mock_sql.connect.called,
                         "Connect shouldn't have been called")

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    @patch('DatabaseHandler.sql')
    def test_handler_constructor_doesnt_init_db_if_full_is_false(self,
                                                                 mock_sql,
                                                                 mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3', full=False)
        self.assertFalse(mock_init_db.called,
                         "initialize_db shouldn't have been called")

    # initialize_db tests
    def test_construct_db_calls_add_address_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        mock_add_addresses = Mock()
        handler._add_addresses_table = mock_add_addresses
        mock_add_stops = Mock()
        handler._add_stops_table = mock_add_stops
        handler.initialize_db()
        self.assertTrue(mock_add_addresses.called,
                        "initialize_db did not call _add_addresses_table")

    def test_construct_db_calls_add_stop_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        mock_add_addresses = Mock()
        handler._add_addresses_table = mock_add_addresses
        mock_add_stops = Mock()
        handler._add_stops_table = mock_add_stops
        handler.initialize_db()
        self.assertTrue(mock_add_stops.called,
                        "initialize_db did not call _add_stops_table")

    def test_construct_db_calls_add_route_table(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        mock_add_addresses = Mock()
        handler._add_addresses_table = mock_add_addresses
        mock_add_stops = Mock()
        handler._add_stops_table = mock_add_stops
        mock_add_routes = Mock()
        handler._add_routes_table = mock_add_routes
        handler.initialize_db()
        self.assertTrue(mock_add_routes.called,
                        "initialize_db did not call _add_routes_table")

    # table construction tests
    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_add_addresses_table_adds_table(self,
                                            mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_addresses_table()
        c = handler.conn.cursor()
        c.execute("SELECT NAME FROM sqlite_master WHERE "
                  "TYPE='table' and NAME='addresses'")
        self.assertTrue(c.fetchone(), "addresses table not created")

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_add_stops_table_adds_table(self,
                                        mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_stops_table()
        c = handler.conn.cursor()
        c.execute("SELECT NAME FROM sqlite_master WHERE "
                  "TYPE='table' and NAME='stops'")
        self.assertTrue(c.fetchone(), "stops table not created")

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_add_routes_table_adds_table(self,
                                         mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_routes_table()
        c = handler.conn.cursor()
        c.execute("SELECT NAME FROM sqlite_master WHERE "
                  "TYPE='table' AND NAME='routes'")
        self.assertTrue(c.fetchone(), "routes table not created")

    # add information to table from file tests

    # Why do the following two tests pass? They shouldn't have the tables.
    # Does pandas.DataFrame.to_sql() create the table if it doesn't find it?

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_handler_add_addresses_from_file_inserts_one_record(self,
                                                                mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        with open('test_file.csv', 'w') as f:
            f.write('latitude,longitude\n')
            f.write('8,12\n')
        handler.add_addresses_from_file('test_file.csv')
        c = handler.conn.cursor()
        c.execute("SELECT latitude, longitude FROM addresses")
        row = c.fetchone()
        self.assertEqual((8, 12), row)

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_handler_add_stops_from_file_inserts_one_record(self,
                                                            mock_init_db):
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
    # add_address tests
    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_add_address_adds_to_address_table(self,
                                               mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_addresses_table()
        handler.add_address(location=MapLocation(latitude=0.56, longitude=9.5))
        c = handler.conn.cursor()
        c.execute("SELECT latitude, longitude FROM addresses")
        row = c.fetchone()
        self.assertEqual((0.56, 9.5), row)

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_add_address_errors_if_location_doesnt_have_latitude(self,
                                                                 mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        self.assertRaises(TypeError, handler.add_address, "15")

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_add_address_uses_MapLocation_id_if_nonzero(self,
                                                        mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_addresses_table()
        address_location = MapLocation(latitude=0.33, longitude=4, id=100)
        handler.add_address(address_location)
        c = handler.conn.cursor()
        c.execute("SELECT * FROM addresses")
        self.assertEqual(100, c.fetchone()[0])

    # add_stop tests
    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_add_stop_adds_to_stops_table(self,
                                          mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_stops_table()
        map_location = MapLocation(latitude=-0.55, longitude=80)
        handler.add_stop(location=map_location)
        c = handler.conn.cursor()
        c.execute("SELECT latitude, longitude FROM stops")
        row = c.fetchone()
        self.assertEqual((-.55, 80), row)

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_add_stop_errors_if_location_is_not_map_location(self,
                                                             mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        self.assertRaises(TypeError, handler.add_stop, 13)

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_add_stop_uses_MapLocation_id_if_nonzero(self,
                                                     mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_stops_table()
        stop_location = MapLocation(latitude=0.48, longitude=179, id=888)
        handler.add_stop(stop_location)
        c = handler.conn.cursor()
        c.execute("SELECT * FROM stops")
        self.assertEqual(888, c.fetchone()[0])

    # add_route tests
    def test_add_route_adds_route(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.add_address(location=MapLocation(latitude=5, longitude=5))
        handler.add_stop(location=MapLocation(latitude=2, longitude=2))
        handler.add_route(address=1, stop=1, distance=10, time=20)
        c = handler.conn.cursor()
        c.execute("SELECT * FROM routes")
        self.assertEqual((1, 1, 1, 10, 20), c.fetchone())

    # Information Retrieval Tests
    # get_address_generator tests
    def test_get_address_without_route_generator_returns_generator(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        self.assertIsInstance(handler.get_address_generator(),
                              types.GeneratorType)

    def test_get_address_without_route_generator_yield_MapLocations(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.add_address(location=MapLocation(latitude=1, longitude=1))
        address_generator = handler.get_address_generator()
        self.assertIsInstance(address_generator.next(), MapLocation)

    def test_get_address_without_route_returns_address_when_routes_empty(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.add_address(location=MapLocation(latitude=5, longitude=6, id=1))
        address_generator = handler.get_address_generator()
        self.assertEqual(MapLocation(latitude=5, longitude=6, id=1),
                         address_generator.next(),
                         "Only MapLocation in addresses was not returned")

    def test_get_address_without_route_returns_with_correct_id(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.add_address(MapLocation(latitude=2, longitude=2, id=222))
        address_generator = handler.get_address_generator()
        self.assertEqual(MapLocation(latitude=2, longitude=2, id=222),
                         address_generator.next(),
                         "MapLocation should return correct id")

    def test_get_address_without_route_returns_address_without_route(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.add_address(location=MapLocation(latitude=1, longitude=2))
        handler.add_address(location=MapLocation(latitude=3, longitude=4))
        handler.add_stop(location=MapLocation(latitude=0, longitude=0))
        c = handler.conn.cursor()
        c.execute("INSERT INTO routes (address_id, stop_id, distance, time)"
                  "VALUES (1, 1, 1, 1)")
        c.close()
        address_generator = handler.get_address_generator()
        self.assertEqual(MapLocation(latitude=3, longitude=4, id=2),
                         address_generator.next(),
                         "the MapLocation without route was not returned")

    def test_get_address_without_route_generator_new_address_second_time(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.add_address(location=MapLocation(latitude=1, longitude=1))
        handler.add_address(location=MapLocation(latitude=2, longitude=2))
        address_generator = handler.get_address_generator()
        self.assertEqual(MapLocation(latitude=1, longitude=1, id=1),
                         address_generator.next(),
                         "first returned MapLocation was not correct")
        self.assertEqual(MapLocation(latitude=2, longitude=2, id=2),
                         address_generator.next(),
                         "second returned MapLocation was not correct")

    # get_all_stops tests
    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_get_all_stops_returns_list_of_MapLocations(self,
                                                        mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_stops_table()
        handler.add_stop(MapLocation(latitude=5, longitude=6))
        handler.add_stop(MapLocation(latitude=3, longitude=-5))
        stops = handler.get_all_stops()
        self.assertEqual((5, 6), (stops[0].latitude, stops[0].longitude))
        self.assertEqual((3, -5), (stops[1].latitude, stops[1].longitude))

    # output_routes tests
    def test_output_routes_outputs_correctly_for_one_route(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.initialize_db()
        handler.add_address(MapLocation(latitude=3, longitude=4, id=1))
        handler.add_stop(MapLocation(latitude=9, longitude=10, id=1))
        handler.add_route(address=1, stop=1, distance=50, time=100)

        handler.output_routes(file_path='test_file.csv')
        self.assertTrue(os.path.exists('test_file.csv'),
                        'test_file.csv file not found')
        output = pd.read_csv('test_file.csv')
        self.assertNotEqual(0, output.shape[0], "no output rows in output .csv")
        self.assertEqual(3, output.ix[0, 'address_latitude'],
                         'incorrect address latitude output')
        self.assertEqual(4, output.ix[0, 'address_longitude'],
                         'incorrect address longitude output')
        self.assertEqual(9, output.ix[0, 'stop_latitude'],
                         'incorrect stop latitude output')
        self.assertEqual(10, output.ix[0, 'stop_longitude'],
                         'incorrect stop longitude output')
        self.assertEqual(50, output.ix[0, 'distance'],
                         'incorrect distance output')
        self.assertEqual(100, output.ix[0, 'time'],
                         'incorrect time output')

    def test_output_routes_calls_correct_function_when_closest_stop_true(self):
        handler = DatabaseHandler(full=False)

        handler.routes_dataframe = Mock()
        handler.routes_dataframe_closest_stops = Mock()

        handler.output_routes(file_path="test_file.csv",
                              closest_stops_only=True)

        handler.routes_dataframe_closest_stops.assert_called_once_with()
        self.assertEqual(0, handler.routes_dataframe.call_count,
                         "routes_dataframe should not be called")

    # routes_dataframe tests
    def test_routes_dataframe_has_correct_values(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.initialize_db()
        handler.add_address(MapLocation(latitude=11, longitude=50, id=11))
        handler.add_stop(MapLocation(latitude=-10, longitude=3, id=800))
        handler.add_route(address=11, stop=800, distance=10000, time=50000)
        df = handler.routes_dataframe()
        self.assertEqual(1, df.shape[0], "only one row should be output")
        self.assertEqual(11, df.ix[0, 'address_latitude'],
                         'incorrect address latitude output')
        self.assertEqual(50, df.ix[0, 'address_longitude'],
                         'incorrect address longitude output')
        self.assertEqual(-10, df.ix[0, 'stop_latitude'],
                         'incorrect stop latitude output')
        self.assertEqual(3, df.ix[0, 'stop_longitude'],
                         'incorrect stop longitude output')
        self.assertEqual(10000, df.ix[0, 'distance'],
                         'incorrect distance output')
        self.assertEqual(50000, df.ix[0, 'time'],
                         'incorrect time output')

    def test_routes_dataframe_only_grabs_routes_no_dangling_locations(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.initialize_db()
        handler.add_address(MapLocation(latitude=1, longitude=1, id=1))
        handler.add_address(MapLocation(latitude=2, longitude=2, id=2))
        handler.add_address(MapLocation(latitude=3, longitude=3, id=3))
        handler.add_stop(MapLocation(latitude=11, longitude=11, id=11))
        handler.add_stop(MapLocation(latitude=12, longitude=12, id=12))
        handler.add_stop(MapLocation(latitude=13, longitude=13, id=13))
        handler.add_route(address=1, stop=11, distance=100, time=1000)
        handler.add_route(address=3, stop=13, distance=100, time=1000)
        df = handler.routes_dataframe()
        self.assertEqual(2, df.shape[0], "should be 2 output rows")
        self.assertEqual(1, df.ix[0, 'address_latitude'],
                         'incorrect address latitude output')
        self.assertEqual(3, df.ix[1, 'address_latitude'],
                         'incorrect address latitude output')
        self.assertEqual(11, df.ix[0, 'stop_latitude'],
                         'incorrect stop latitude output')
        self.assertEqual(13, df.ix[1, 'stop_latitude'],
                         'incorrect stop latitude output')

    # routes_dataframe_closest_stops tests
    def test_routes_dataframe_closest_stops_returns_closest_stop(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.initialize_db()
        handler.add_address(MapLocation(latitude=1, longitude=1, id=1))
        handler.add_stop(MapLocation(latitude=2, longitude=2, id=2))
        handler.add_stop(MapLocation(latitude=3, longitude=3, id=3))
        handler.add_route(address=1, stop=2, distance=100, time=100)
        handler.add_route(address=1, stop=3, distance=50, time=50)
        df = handler.routes_dataframe_closest_stops()
        self.assertEqual(1, df.shape[0], "should be 1 output row")
        self.assertEqual(1, df.ix[0, 'address_latitude'],
                         'address should have latitude of 1')
        self.assertEqual(1, df.ix[0, 'address_longitude'],
                         'address should have longitude of 1')
        self.assertEqual(3, df.ix[0, 'stop_latitude'],
                         'the stop with latitude of 3 should have been '
                         'returned since it had the smallest distance')
        self.assertEqual(3, df.ix[0, 'stop_longitude'],
                         'the stop with longitude of 3 should have been '
                         'returned since it had the smallest distance')
        self.assertEqual(50, df.ix[0, 'distance'],
                         "the route with the lowest distance should be"
                         "returned in the output dataframe")
        self.assertEqual(50, df.ix[0, 'time'],
                         "the route the with lowest distance's time should be"
                         "returned in the output dataframe")

    def test_routes_dataframe_closest_stops_returns_for_many_addresses(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.initialize_db()
        handler.add_address(MapLocation(latitude=1, longitude=1, id=1))
        handler.add_address(MapLocation(latitude=11, longitude=10, id=11))
        handler.add_stop(MapLocation(latitude=2, longitude=2, id=2))
        handler.add_stop(MapLocation(latitude=12, longitude=12, id=12))
        handler.add_route(address=1, stop=2, distance=1, time=1)
        handler.add_route(address=1, stop=12, distance=11, time=11)
        handler.add_route(address=11, stop=2, distance=9, time=9)
        handler.add_route(address=11, stop=12, distance=1, time=1)
        df = handler.routes_dataframe_closest_stops()
        self.assertEqual(2, df.shape[0], "should be 2 output rows since "
                                         "there are 2 addresses with routes")
        self.assertEqual(1, df.ix[0, 'distance'],
                         "distance for the first row should be 1 "
                         "since that is the shortest route distance")
