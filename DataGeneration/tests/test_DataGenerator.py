from DataGeneration import DataGenerator
from DataGeneration import DatabaseHandler
from DataGeneration import MapLocation
from DataGeneration import MapboxAPIWrapper
import unittest
from mock import Mock, patch, MagicMock


class test_DataGenerator(unittest.TestCase):

    # __init__ tests
    def test_DataGenerator_exists(self):
        generator = DataGenerator()
        self.assertIsInstance(generator, DataGenerator)

    def test_constructor_sets_stops_array_to_empty_list(self):
        generator = DataGenerator()
        self.assertEqual([], generator.stops)

    def test_constructor_sets_handler_to_simple_handler(self):
        generator = DataGenerator()
        self.assertIsInstance(generator.handler, DatabaseHandler)

    def test_constructor_sets_wrapper_instance_variable(self):
        generator = DataGenerator()
        self.assertIsInstance(generator.wrapper, MapboxAPIWrapper)

    # initialize tests
    @patch('DataGeneration.DataGenerator.get_api_wrapper')
    @patch('DataGeneration.DatabaseHandler.get_all_stops')
    @patch('DataGeneration.DataGenerator.get_database_handler')
    def test_initialize_initializes_database(self,
                                        mock_get_db,
                                        mock_get_all_stops,
                                        mock_get_api_wrapper):
        generator = DataGenerator()
        mock_get_db.return_value = DatabaseHandler(full=False)
        generator.initialize()
        mock_get_db.assert_called_once_with('db.sqlite3')

    @patch('DataGeneration.DataGenerator.get_api_wrapper')
    @patch('DataGeneration.DatabaseHandler.get_all_stops')
    @patch('DataGeneration.DataGenerator.get_database_handler')
    def test_initialize_pulls_all_stops(self,
                                   mock_get_db,
                                   mock_get_all_stops,
                                   mock_get_api_wrapper):
        generator = DataGenerator()
        mock_get_db.return_value = DatabaseHandler(full=False)
        generator.initialize()
        mock_get_all_stops.assert_called_once_with()

    @patch('DataGeneration.DataGenerator.get_api_wrapper')
    @patch('DataGeneration.DatabaseHandler.get_all_stops')
    @patch('DataGeneration.DataGenerator.get_database_handler')
    def test_initialize_initializes_api_wrapper(self,
                                           mock_get_db,
                                           mock_get_all_stops,
                                           mock_get_api_wrapper):
        generator = DataGenerator()
        mock_get_db.return_value = DatabaseHandler(full=False)
        generator.initialize()
        mock_get_api_wrapper.assert_called_once_with('api_key.txt')

    # get_database_handler tests
    def test_get_database_handler_returns_DatabaseHandler(self):
        generator = DataGenerator()
        self.assertIsInstance(generator.get_database_handler(), DatabaseHandler)

    # get_api_wrapper tests
    @patch('DataGeneration.MapboxAPIWrapper.load_api_key_from_file')
    def test_get_api_wrapper_returns_MapboxAPIWrapper(self,
                                                      mock_get_key):
        generator = DataGenerator()
        self.assertIsInstance(generator.get_api_wrapper(), MapboxAPIWrapper)

    @patch('DataGeneration.MapboxAPIWrapper.load_api_key_from_file')
    def test_get_api_wrapper_pulls_api_key(self,
                                           mock_get_key):
        generator = DataGenerator()
        generator.get_api_wrapper()
        mock_get_key.assert_called_once_with('api_key.txt')

    # begin tests
    @patch('DataGeneration.DatabaseHandler.get_all_stops')
    @patch('DataGeneration.DatabaseHandler.get_address_without_route_generator')
    def test_begin_calls_handler_get_next_address(self,
                                                  mock_get_address,
                                                  mock_get_all_stops):
        generator = DataGenerator()
        generator.begin()

        mock_get_address.assert_called_once_with()

    @patch('DataGeneration.DatabaseHandler.get_all_stops')
    @patch('DataGeneration.DatabaseHandler.get_address_without_route_generator')
    def test_begin_calls_get_all_stops(self,
                                       mock_get_address,
                                       mock_get_all_stops):
        generator = DataGenerator()
        generator.begin()
        mock_get_all_stops.assert_called_once_with()

    @patch('DataGeneration.DatabaseHandler.get_all_stops')
    @patch('DataGeneration.DatabaseHandler.get_address_without_route_generator')
    def test_begin_calls_get_closest_locations(self,
                                               mock_get_address,
                                               mock_get_all_stops):
        generator = DataGenerator()

        address = MapLocation(1, 1, 1)
        mock_get_address.return_value = [address]  # List to emulate generator

        stops = [MapLocation(2, 2, 2), MapLocation(3, 3, 3)]
        mock_get_all_stops.return_value = stops

        mock_get_closest_locations = Mock(return_value=[stops[0]])
        generator.get_closest_locations = mock_get_closest_locations

        generator.wrapper.get_distance_from_api = Mock()

        generator.begin(stops_to_query=1)
        mock_get_closest_locations.assert_called_once_with(address, stops, n=1)

    @patch('DataGeneration.DatabaseHandler.get_all_stops')
    @patch('DataGeneration.DatabaseHandler.get_address_without_route_generator')
    def test_begin_calls_wrapper_get_distance_from_api(self,
                                                       mock_get_address,
                                                       mock_get_all_stops):
        generator = DataGenerator()

        address = MapLocation(1, 1, 1)
        mock_get_address.return_value = [address]  # List to emulate generator

        stops = [MapLocation(2, 2, 2), MapLocation(3, 3, 3)]
        mock_get_all_stops.return_value = stops

        generator.get_closest_locations = Mock(return_value=[stops[0]])

        mock_get_distance = Mock()
        generator.wrapper.get_distance_from_api = mock_get_distance

        generator.begin(stops_to_query=1)
        mock_get_distance.assert_called_once_with(address, stops[0])

    # get_closest_locations tests
    def test_get_closest_locations_returns_closest_single_location_1(self):
        generator = DataGenerator()
        stops = [MapLocation(1, 1, 1),
                 MapLocation(2, 2, 2)]
        address = MapLocation(0, 0, 0)
        closest_stops = generator.get_closest_locations(source=address,
                                                        destinations=stops,
                                                        n=1)
        self.assertEqual(MapLocation(1, 1, 1), closest_stops[0],
                         "{}, should be 1, 1".format(closest_stops[0]))

    def test_get_closest_locations_returns_closest_single_location_2(self):
        generator = DataGenerator()
        stops = [MapLocation(3, 3, 3),
                 MapLocation(4, 4, 4)]
        address = MapLocation(5, 5, 5)
        closest_stops = generator.get_closest_locations(source=address,
                                                        destinations=stops,
                                                        n=1)
        self.assertEqual(MapLocation(4, 4, 4), closest_stops[0],
                         "{}, should be 4, 4".format(closest_stops[0]))

    def test_get_closest_locations_returns_closest_2_locations(self):
        generator = DataGenerator()
        stops = [MapLocation(1, 1, 1),
                 MapLocation(5, 5, 5),
                 MapLocation(6, 6, 6)]
        address = MapLocation(4, 4, 4)
        closest_stops = generator.get_closest_locations(source=address,
                                                        destinations=stops,
                                                        n=2)
        self.assertEqual(MapLocation(5, 5, 5), closest_stops[0],
                         "{}, should be 5, 5".format(closest_stops[0]))
        self.assertEqual(MapLocation(6, 6, 6), closest_stops[1],
                         "{}, should be 6, 6".format(closest_stops[1]))

    def test_get_closest_locations_returns_location_when_equal(self):
        generator = DataGenerator()
        stops = [MapLocation(1, 1, 1),
                 MapLocation(3, 3, 3)]
        address = MapLocation(2, 2, 2)
        closest_stops = generator.get_closest_locations(source=address,
                                                        destinations=stops,
                                                        n=1)
        self.assertEqual(MapLocation(1, 1, 1), closest_stops[0],
                         "{}, should be 1, 1".format(closest_stops[0]))
