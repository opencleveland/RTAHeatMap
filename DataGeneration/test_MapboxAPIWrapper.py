import unittest, mock
from mock import patch, mock_open
from MapboxAPIWrapper import MapboxAPIWrapper
from MapLocation import MapLocation

from sys import version_info
if version_info.major == 2:
    import __builtin__ as builtins
else:
    import builtins

class TestMapboxAPIWrapper(unittest.TestCase):

    def test_mapbox_api_wrapper_class_exists(self):
        wrapper = MapboxAPIWrapper()
        self.assertIsInstance(wrapper, MapboxAPIWrapper)

    # load_api_key_from_file tests
    @patch('MapboxAPIWrapper.os.path')
    def test_mapbox_load_api_key_checks_for_file_existance(self, mock_os_path):
        wrapper = MapboxAPIWrapper()
        mock_os_path.exists.return_value = True
        with patch.object(builtins, 'open', mock_open(read_data='api_key')):
            wrapper.load_api_key_from_file()
        self.assertTrue(mock_os_path.exists.called, "os.path.exists was not called")

    @patch('MapboxAPIWrapper.os.path')
    def test_mapbox_load_api_key_from_file_fails_bad_path(self, mock_os_path):
        mock_os_path.exists.return_value = False
        wrapper = MapboxAPIWrapper()
        self.assertRaises(ValueError, wrapper.load_api_key_from_file)

    @patch('MapboxAPIWrapper.os.path')
    def test_mapbox_load_api_key_from_file_opens_file(self, mock_os_path):
        mock_os_path.exists.return_value = True
        wrapper = MapboxAPIWrapper()
        with patch.object(builtins, 'open', mock_open(read_data='api_key')):
            wrapper.load_api_key_from_file(filename='abc.txt')
        self.assertEquals('api_key', wrapper.key)

    # set_origin_location tests
    def test_mapbox_set_origin_location_is_MapLocation(self):
        wrapper = MapboxAPIWrapper()
        wrapper.set_origin_location(MapLocation())
        self.assertIsInstance(wrapper.origin, MapLocation)

    def test_mapbox_set_origin_location_errors_for_wrong_type(self):
        wrapper = MapboxAPIWrapper()
        self.assertRaises(TypeError, wrapper.set_origin_location, "string")

    # set_destination_location tests
    def test_mapbox_set_destination_location_is_MapLocation(self):
        wrapper = MapboxAPIWrapper()
        wrapper.set_destination_location(MapLocation())
        self.assertIsInstance(wrapper.destination, MapLocation)

    def test_mapbox_set_destination_location_errors_for_wrong_type(self):
        wrapper = MapboxAPIWrapper()
        self.assertRaises(TypeError, wrapper.set_destination_location, "string")

    # construct_request_string tests
    def test_construct_request_string_returns_string(self):
        wrapper = MapboxAPIWrapper()
        wrapper.origin = MapLocation()
        wrapper.destination = MapLocation()
        wrapper.key = 'api_key'
        self.assertIsInstance(wrapper.construct_request_string(), str)

    def test_construct_request_string_errors_if_no_origin(self):
        wrapper = MapboxAPIWrapper()
        wrapper.destination = MapLocation()
        wrapper.key = 'api_key'
        self.assertRaises(UnboundLocalError, wrapper.construct_request_string)

    def test_construct_request_string_errors_if_no_destination(self):
        wrapper = MapboxAPIWrapper()
        wrapper.origin = MapLocation()
        wrapper.key = 'api_key'
        self.assertRaises(UnboundLocalError, wrapper.construct_request_string)

    def test_constuct_request_string_errors_if_no_key(self):
        wrapper = MapboxAPIWrapper()
        wrapper.origin = MapLocation()
        wrapper.destination = MapLocation()
        self.assertRaises(UnboundLocalError, wrapper.construct_request_string)

    def test_construct_request_string_produces_correct_output(self):
        wrapper = MapboxAPIWrapper()
        wrapper.origin = MapLocation(latitude = 50.032,
                                     longitude = 40.54453)
        wrapper.destination = MapLocation(latitude = 51.0345,
                                          longitude = 41.2314)
        wrapper.key = 'api_key'
        self.assertEqual('https://api.mapbox.com/v4/directions/mapbox.walking/'
                         '50.032,40.54453;51.0345,41.2314.json?alternatives='
                         'false&instructions=text&geometry=false&steps=false&&'
                         'access_token=api_key',
                         wrapper.construct_request_string())

    # get_dstiance_from_api tests
    @patch('MapboxAPIWrapper.MapboxAPIWrapper.construct_request_string')
    def test_get_distance_from_api_constructs_request_string(self,
                                                             mock_construct):
        mock_construct.return_value = 'api_request'
        wrapper = MapboxAPIWrapper()
        wrapper.get_distance_from_api()
        self.assertTrue(mock_construct.called, 'api call must construct '
                                                    'request string')

    # make_api_call tests
    #def test_make_api_call_returns_string(self):
    #    wrapper = MapboxAPIWrapper()
    #    self.assertIsInstance(wrapper.make_api_call('request_string'), tuple)

    @patch('MapboxAPIWrapper.urlopen')
    def test_make_api_call_calls_urlopen(self, mock_urlopen):
        mock_urlopen.return_value = 'response_string'
        wrapper = MapboxAPIWrapper()
        wrapper.make_api_call('request_string')
        self.assertTrue(mock_urlopen.called, 'make_api_call must call urlopen')
