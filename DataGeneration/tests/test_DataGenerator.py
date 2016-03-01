from DataGeneration import DataGenerator
from DataGeneration import DatabaseHandler
from DataGeneration import MapLocation
from DataGeneration import MapboxAPIWrapper
from MapboxAPIWrapper import MapboxAPIError
import unittest
from mock import Mock, patch, MagicMock


class test_DataGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = DataGenerator()

    # __init__ tests
    def test_DataGenerator_exists(self):
        self.assertIsInstance(self.generator, DataGenerator)

    def test_constructor_sets_stops_array_to_empty_list(self):
        self.assertEqual([], self.generator.stops)

    def test_constructor_sets_handler_to_simple_handler(self):
        self.assertIsInstance(self.generator.handler, DatabaseHandler)

    def test_constructor_sets_wrapper_instance_variable(self):
        self.assertIsInstance(self.generator.wrapper, MapboxAPIWrapper)

    # initialize tests
    def test_initialize_initializes_database(self):
        self.generator._get_database_handler = Mock()
        self.generator.handler.get_all_stops = Mock()
        self.generator._get_api_wrapper = Mock()

        self.generator.initialize()
        self.generator._get_database_handler.assert_called_once_with('db.sqlite3')

    def test_initialize_pulls_all_stops(self):
        self.generator._get_database_handler = Mock()
        self.generator.handler.get_all_stops = Mock()
        self.generator._get_api_wrapper = Mock()

        self.generator.initialize()
        self.generator.handler.get_all_stops.assert_called_once_with()

    def test_initialize_initializes_api_wrapper(self):
        self.generator._get_database_handler = Mock()
        self.generator.handler.get_all_stops = Mock()
        self.generator._get_api_wrapper = Mock()

        self.generator.initialize()
        self.generator._get_api_wrapper.assert_called_once_with('api_key.txt')

    # _get_database_handler tests
    @patch('DataGeneration.DatabaseHandler.__init__')
    def test_get_database_handler_returns_DatabaseHandler(self,
                                                          mock_init):
        mock_init.return_value = None
        self.assertIsInstance(self.generator._get_database_handler(),
                              DatabaseHandler)

    @patch('DataGeneration.DatabaseHandler.__init__')
    def test_get_database_handler_inits_DatabaseHandler(self,
                                                        mock_init):
        mock_init.return_value = None
        self.generator._get_database_handler()
        mock_init.assert_called_once_with('db.sqlite3')

    @patch('DataGeneration.DatabaseHandler.__init__')
    def test_get_database_handler_inits_DatabaseHandler_with_db(self,
                                                                mock_init):
        mock_init.return_value = None
        self.generator._get_database_handler(db_file_name='test_db')
        mock_init.assert_called_once_with('test_db')

    # _get_api_wrapper tests
    @patch('DataGeneration.MapboxAPIWrapper.load_api_key_from_file')
    def test_get_api_wrapper_returns_MapboxAPIWrapper(self,
                                                      mock_get_key):
        self.assertIsInstance(self.generator._get_api_wrapper(),
                              MapboxAPIWrapper)

    @patch('DataGeneration.MapboxAPIWrapper.load_api_key_from_file')
    def test_get_api_wrapper_pulls_api_key(self,
                                           mock_get_key):
        self.generator._get_api_wrapper()
        mock_get_key.assert_called_once_with('api_key.txt')

    # begin tests
    def test_begin_calls_handler_get_next_address(self):
        self.generator.handler.get_address_generator = MagicMock()

        self.generator.begin(verbose=False)
        self.generator.handler.get_address_generator.\
            assert_called_once_with(verbose=False)

    def test_begin_calls_get_closest_locations(self):
        addresses = MapLocation(1, 1, 1)
        self.generator.handler.get_address_generator = \
            MagicMock(return_value=[addresses])

        self.generator.stops = [MapLocation(2, 2, 2), MapLocation(3, 3, 3)]

        mock_get_closest_locations = Mock(return_value=[self.generator.stops[0]])
        self.generator._get_closest_locations = mock_get_closest_locations

        self.generator.wrapper.get_distance_from_api = \
            Mock(return_value={"distance": 6, "time": 9})
        self.generator.handler.add_route = Mock()

        self.generator.begin(stops_per_address=1, verbose=False)
        mock_get_closest_locations.assert_called_once_with(addresses,
                                                           self.generator.stops,
                                                           n=1)

    def test_begin_calls_wrapper_get_distance_from_api(self):
        addresses = MapLocation(1, 1, 1)
        self.generator.handler.get_address_generator = \
            MagicMock(return_value=[addresses])

        self.generator.stops = [MapLocation(2, 2, 2), MapLocation(3, 3, 3)]

        self.generator._get_closest_locations = \
            Mock(return_value=[self.generator.stops[0]])

        mock_get_distance = Mock(return_value={"distance": 6, "time": 9})
        self.generator.wrapper.get_distance_from_api = mock_get_distance

        self.generator.handler.add_route = Mock()

        self.generator.begin(stops_per_address=1, verbose=False)
        mock_get_distance.assert_called_once_with(addresses,
                                                  self.generator.stops[0])

    def test_begin_inserts_api_results_into_db(self):
        addresses = MapLocation(1, 1, 1)
        self.generator.handler.get_address_generator = \
            MagicMock(return_value=[addresses])

        self.generator.stops = [MapLocation(2, 2, 2), MapLocation(3, 3, 3)]

        self.generator._get_closest_locations = \
            Mock(return_value=[self.generator.stops[0]])

        self.generator.wrapper.get_distance_from_api = \
            Mock(return_value={"distance": 6, "time": 9})

        self.generator.handler.add_route = Mock()

        self.generator.begin(stops_per_address=1, verbose=False)

        self.generator.handler.add_route.assert_called_once_with(1, 2, 6, 9)

    @patch('DataGeneration.MapboxAPIWrapper.get_distance_from_api')
    def test_begin_doesnt_call_add_route_if_MapboxAPIError_occurs(self,
                                                                  mock_api):
        addresses = MapLocation(1, 1, 1)
        self.generator.handler.get_address_generator = \
            MagicMock(return_value=[addresses])

        self.generator.stops = [MapLocation(2, 2, 2)]

        self.generator._get_closest_locations = \
            Mock(return_value=[self.generator.stops[0]])

        # force get_distance_from_api to raise a MapboxAPIError exception
        mock_api.side_effect = MapboxAPIError("API Error")

        mock_add_route = Mock()
        self.generator.handler.add_route = mock_add_route

        self.generator.begin(stops_per_address=1, verbose=False)

        mock_add_route.assert_not_called()

    # get_closest_locations tests
    def test_get_closest_locations_returns_closest_single_location_1(self):
        generator = DataGenerator()
        stops = [MapLocation(1, 1, 1),
                 MapLocation(2, 2, 2)]
        address = MapLocation(0, 0, 0)
        closest_stops = generator._get_closest_locations(source=address,
                                                         destinations=stops,
                                                         n=1)
        self.assertEqual(MapLocation(1, 1, 1), closest_stops[0],
                         "{}, should be 1, 1".format(closest_stops[0]))

    def test_get_closest_locations_returns_closest_single_location_2(self):
        generator = DataGenerator()
        stops = [MapLocation(3, 3, 3),
                 MapLocation(4, 4, 4)]
        address = MapLocation(5, 5, 5)
        closest_stops = generator._get_closest_locations(source=address,
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
        closest_stops = generator._get_closest_locations(source=address,
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
        closest_stops = generator._get_closest_locations(source=address,
                                                         destinations=stops,
                                                         n=1)
        self.assertEqual(MapLocation(1, 1, 1), closest_stops[0],
                         "{}, should be 1, 1".format(closest_stops[0]))
