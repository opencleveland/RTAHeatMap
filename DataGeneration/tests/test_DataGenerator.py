from DataGeneration import DataGenerator
from DataGeneration import DatabaseHandler
from DataGeneration import MapLocation
from DataGeneration import MapboxAPIWrapper
from MapboxAPIWrapper import MapboxAPIError
import unittest
from mock import Mock, patch, MagicMock, mock


class test_DataGenerator(unittest.TestCase):

    def setUp(self):
        self.generator = DataGenerator(handler=DatabaseHandler(full=False),
                                       stops=[],
                                       wrapper=MapboxAPIWrapper())

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

    def test_begin_calls_process_stop_for_each_stop(self):
        address = MapLocation(1, 1, 1)
        self.generator.handler.get_address_generator = \
            MagicMock(return_value=[address])

        stops = [MapLocation(2, 2, 2), MapLocation(3, 3, 3)]

        mock_get_closest_locations = Mock(return_value=stops)
        self.generator._get_closest_locations = mock_get_closest_locations

        mock_process_stop = Mock()
        self.generator.process_stop = mock_process_stop

        self.generator.begin(stops_per_address=2, verbose=False)

        self.assertEqual(2, mock_process_stop.call_count)

        expected_calls = [mock.call(address, stops[0], False, 'walking'),
                          mock.call(address, stops[1], False, 'walking')]
        self.assertEqual(expected_calls, mock_process_stop.call_args_list)

    def test_begin_calls_process_stop_for_each_stop_with_mode(self):
        address = MapLocation(1, 1, 1)
        self.generator.handler.get_address_generator = \
            MagicMock(return_value=[address])

        stops = [MapLocation(2, 2, 2), MapLocation(3, 3, 3)]

        mock_get_closest_locations = Mock(return_value=stops)
        self.generator._get_closest_locations = mock_get_closest_locations

        mock_process_stop = Mock()
        self.generator.process_stop = mock_process_stop

        self.generator.begin(stops_per_address=2, verbose=False, mode='driving')

        self.assertEqual(2, mock_process_stop.call_count)

        expected_calls = [mock.call(address, stops[0], False, 'driving'),
                          mock.call(address, stops[1], False, 'driving')]
        self.assertEqual(expected_calls, mock_process_stop.call_args_list)

    def test_begin_doesnt_call_add_route_if_MapboxAPIError_occurs(self):
        addresses = MapLocation(1, 1, 1)
        self.generator.handler.get_address_generator = \
            MagicMock(return_value=[addresses])

        self.generator.wrapper.get_distance_from_api = Mock()

        self.generator.stops = [MapLocation(2, 2, 2)]

        self.generator._get_closest_locations = \
            Mock(return_value=[self.generator.stops[0]])

        # force get_distance_from_api to raise a MapboxAPIError exception
        self.generator.wrapper.get_distance_from_api.\
            side_effect = MapboxAPIError("API Error")

        mock_add_route = Mock()
        self.generator.handler.add_route = mock_add_route

        self.generator.begin(stops_per_address=1, verbose=False)

        mock_add_route.assert_not_called()

    # process_stop tests
    def test_process_stop_calls_get_distance_from_api(self):
        mock_get_distance = Mock(return_value={"distance": 6, "time": 9})
        self.generator.wrapper.get_distance_from_api = mock_get_distance

        self.generator.handler.add_route = Mock()

        address = MapLocation(1, 1, 1)
        stop = MapLocation(2, 2, 2)
        self.generator.process_stop(address=address, stop=stop, verbose=False)

        mock_get_distance.assert_called_once_with(address, stop, 'walking')

    def test_process_stop_calls_get_distance_from_api_with_mode(self):
        mock_get_distance = Mock(return_value={"distance": 6, "time": 9})
        self.generator.wrapper.get_distance_from_api = mock_get_distance

        self.generator.handler.add_route = Mock()

        address = MapLocation(1, 1, 1)
        stop = MapLocation(2, 2, 2)
        self.generator.process_stop(address=address, stop=stop,
                                    verbose=False, mode='driving')

        mock_get_distance.assert_called_once_with(address, stop, 'driving')

    def test_process_stop_calls_add_route(self):
        self.generator.wrapper.get_distance_from_api = \
            Mock(return_value={"distance": 6, "time": 9})

        self.generator.handler.add_route = Mock()

        self.generator.process_stop(address=MapLocation(3, 3, 3),
                                    stop=MapLocation(4, 4, 4),
                                    verbose=False)

        self.generator.handler.add_route.assert_called_once_with(3, 4, 6, 9)

    # get_closest_locations tests
    def test_get_closest_locations_returns_closest_single_location_1(self):
        stops = [MapLocation(1, 1, 1),
                 MapLocation(2, 2, 2)]
        address = MapLocation(0, 0, 0)
        closest = self.generator._get_closest_locations(source=address,
                                                        destinations=stops,
                                                        n=1)
        self.assertEqual(MapLocation(1, 1, 1), closest[0],
                         "{}, should be 1, 1".format(closest[0]))

    def test_get_closest_locations_returns_closest_single_location_2(self):
        stops = [MapLocation(3, 3, 3),
                 MapLocation(4, 4, 4)]
        address = MapLocation(5, 5, 5)
        closest = self.generator._get_closest_locations(source=address,
                                                        destinations=stops,
                                                        n=1)
        self.assertEqual(MapLocation(4, 4, 4), closest[0],
                         "{}, should be 4, 4".format(closest[0]))

    def test_get_closest_locations_returns_closest_2_locations(self):
        stops = [MapLocation(1, 1, 1),
                 MapLocation(5, 5, 5),
                 MapLocation(6, 6, 6)]
        address = MapLocation(4, 4, 4)
        closest = self.generator._get_closest_locations(source=address,
                                                        destinations=stops,
                                                        n=2)
        self.assertEqual(MapLocation(5, 5, 5), closest[0],
                         "{}, should be 5, 5".format(closest[0]))
        self.assertEqual(MapLocation(6, 6, 6), closest[1],
                         "{}, should be 6, 6".format(closest[1]))

    def test_get_closest_locations_returns_location_when_equal(self):
        stops = [MapLocation(1, 1, 1),
                 MapLocation(3, 3, 3)]
        address = MapLocation(2, 2, 2)
        closest = self.generator._get_closest_locations(source=address,
                                                        destinations=stops,
                                                        n=1)
        self.assertEqual(MapLocation(1, 1, 1), closest[0],
                         "{}, should be 1, 1".format(closest[0]))
