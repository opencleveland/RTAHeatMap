import unittest
from mock import patch, MagicMock, Mock
from DatabaseHandler import DatabaseHandler
from DataGeneration.MapLocation import MapLocation
import os


class TestDatabaseHandler(unittest.TestCase):

    def setUp(self):
        if os.path.exists('unit_test_db.sqlite3'):
            os.remove('unit_test_db.sqlite3')

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
    def test_get_address_without_route_returns_MapLocation(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.add_address(location=MapLocation(latitude=5, longitude=6))
        self.assertIsInstance(handler.get_address_without_route(), MapLocation)

    def test_get_address_without_route_returns_address_when_routes_empty(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.add_address(location=MapLocation(latitude=5, longitude=6, id=1))
        self.assertEqual(MapLocation(latitude=5, longitude=6, id=1),
                         handler.get_address_without_route(),
                         "Only MapLocation in addresses was not returned")

    def test_get_address_without_route_returns_with_correct_id(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.add_address(MapLocation(latitude=2, longitude=2, id=222))
        self.assertEqual(MapLocation(latitude=2, longitude=2, id=222),
                         handler.get_address_without_route(),
                         "MapLocation should return correct id")

    def test_get_address_without_route_returns_address_without_route(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.add_address(location=MapLocation(latitude=1, longitude=2))
        handler.add_address(location=MapLocation(latitude=3, longitude=4))
        handler.add_stop(location=MapLocation(latitude=0, longitude=0))
        c = handler.conn.cursor()
        c.execute("INSERT INTO routes (address_id, stop_id, distance, time)"
                  "VALUES (1, 1, 1, 1)")
        self.assertEqual(MapLocation(latitude=3, longitude=4, id=2),
                         handler.get_address_without_route(),
                         "the MapLocation without route was not returned")

    # get_address_without_route_generator tests
    def test_get_address_without_route_new_address_second_time(self):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler.add_address(location=MapLocation(latitude=1, longitude=1))
        handler.add_address(location=MapLocation(latitude=2, longitude=2))
        address_generator = handler.get_address_without_route_generator()
        self.assertEqual(MapLocation(latitude=1, longitude=1, id=1),
                         address_generator.next(),
                         "first returned MapLocation was not correct")
        self.assertEqual(MapLocation(latitude=2, longitude=2, id=2),
                         address_generator.next(),
                         "second returned MapLocation was not correct")

    # id existence tests
    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_address_id_in_table_returns_false_if_not_present(self,
                                                              mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_addresses_table()
        c = handler.conn.cursor()
        c.execute("INSERT INTO addresses VALUES (1, 3, 7)")
        self.assertEqual(False, handler._address_id_in_table(id=2))

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_address_id_in_table_returns_true_if_present(self,
                                                         mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_addresses_table()
        c = handler.conn.cursor()
        c.execute("INSERT INTO addresses VALUES (1, 5, 10)")
        self.assertEqual(True, handler._address_id_in_table(id=1))

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_stop_id_in_table_returns_false_if_not_present(self,
                                                           mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_stops_table()
        c = handler.conn.cursor()
        c.execute("INSERT INTO stops VALUES (1, 3, 7)")
        self.assertEqual(False, handler._stop_id_in_table(id=2))

    @patch('DatabaseHandler.DatabaseHandler.initialize_db')
    def test_stop_id_in_table_returns_true_if_present(self,
                                                      mock_init_db):
        handler = DatabaseHandler('unit_test_db.sqlite3')
        handler._add_stops_table()
        c = handler.conn.cursor()
        c.execute("INSERT INTO stops VALUES (1, 5, 10)")
        self.assertEqual(True, handler._stop_id_in_table(id=1))

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
