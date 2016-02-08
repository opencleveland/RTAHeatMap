import unittest
from mock import patch, mock_open, mock, MagicMock
import requests
from DataGeneration.MapboxAPIWrapper import MapboxAPIWrapper
from DataGeneration.MapLocation import MapLocation


from sys import version_info
if version_info.major == 2:
    import __builtin__ as builtins
else:
    import builtins


class CustomHTTPException(Exception):
    pass


class TestMapboxAPIWrapper(unittest.TestCase):

    def setUp(self):
        self.wrapper = MapboxAPIWrapper()
        self.expected_dict = {
            u'origin': {
                u'geometry': {
                    u'type': u'Point',
                    u'coordinates': [
                        50.032,
                        40.54453
                    ]
                },
                u'type': u'Feature',
                u'properties': {
                    u'name': u'McAllister Street'
                }
            },
            u'routes': [
                {
                    u'duration': 61045,
                    u'distance': 221074,
                    u'steps': [],
                    u'summary': u''
                }
            ],
            u'destination': {
                u'geometry': {
                    u'type': u'Point',
                    u'coordinates': [
                        51.0345,
                        41.2314
                    ]
                },
                u'type': u'Feature',
                u'properties': {
                    u'name': u'Logan Circle Northwest'
                }
            },
            u'waypoints': []}

    def test_mapbox_api_wrapper_class_exists(self):
        self.assertIsInstance(self.wrapper, MapboxAPIWrapper)

    # load_api_key_from_file tests
    @patch('MapboxAPIWrapper.os.path')
    def test_mapbox_load_api_key_checks_for_file_existance(self, mock_os_path):
        mock_os_path.exists.return_value = True
        with patch.object(builtins, 'open', mock_open(read_data='api_key')):
            self.wrapper.load_api_key_from_file()
        mock_os_path.exists.assert_called_once_with('api_key.txt')

    @patch('MapboxAPIWrapper.os.path')
    def test_mapbox_load_api_key_from_file_fails_bad_path(self, mock_os_path):
        mock_os_path.exists.return_value = False
        self.assertRaises(ValueError, self.wrapper.load_api_key_from_file)

    @patch('MapboxAPIWrapper.os.path')
    def test_mapbox_load_api_key_from_file_opens_file(self, mock_os_path):
        mock_os_path.exists.return_value = True
        with patch.object(builtins, 'open', mock_open(read_data='api_key')):
            self.wrapper.load_api_key_from_file(filename='abc.txt')
        self.assertEquals('api_key', self.wrapper.key)

    @patch('MapboxAPIWrapper.os.path')
    def test_mapbox_load_api_key_from_file_accepts_filename(self, mock_os_path):
        mock_os_path.exists.return_value = True
        with patch.object(builtins, 'open', mock_open(read_data='api_key')):
            self.wrapper.load_api_key_from_file(filename='abc.txt')
        mock_os_path.exists.assert_called_once_with('abc.txt')

    # set_origin_location tests
    def test_mapbox_set_origin_location_is_MapLocation(self):
        self.wrapper.set_origin_location(MapLocation())
        self.assertIsInstance(self.wrapper.origin, MapLocation)

    def test_mapbox_set_origin_location_errors_for_wrong_type(self):
        self.assertRaises(TypeError, self.wrapper.set_origin_location, "string")

    # set_destination_location tests
    def test_mapbox_set_destination_location_is_MapLocation(self):
        self.wrapper.set_destination_location(MapLocation())
        self.assertIsInstance(self.wrapper.destination, MapLocation)

    def test_mapbox_set_destination_location_errors_for_wrong_type(self):
        self.assertRaises(TypeError,
                          self.wrapper.set_destination_location, "string")

    # construct_request_string tests
    def test_construct_request_string_returns_string(self):
        self.wrapper.origin = MapLocation()
        self.wrapper.destination = MapLocation()
        self.wrapper.key = 'api_key'
        self.assertIsInstance(self.wrapper.construct_request_string(), str)

    def test_construct_request_string_errors_if_no_origin(self):
        self.wrapper.destination = MapLocation()
        self.wrapper.key = 'api_key'
        self.assertRaises(UnboundLocalError, self.wrapper.construct_request_string)

    def test_construct_request_string_errors_if_no_destination(self):
        self.wrapper.origin = MapLocation()
        self.wrapper.key = 'api_key'
        self.assertRaises(UnboundLocalError,
                          self.wrapper.construct_request_string)

    def test_constuct_request_string_errors_if_no_key(self):
        self.wrapper.origin = MapLocation()
        self.wrapper.destination = MapLocation()
        self.assertRaises(UnboundLocalError,
                          self.wrapper.construct_request_string)

    def test_construct_request_string_produces_correct_output(self):
        self.wrapper.origin = MapLocation(latitude = 50.032,
                                          longitude = 40.54453)
        self.wrapper.destination = MapLocation(latitude = 51.0345,
                                               longitude = 41.2314)
        self.wrapper.key = 'api_key'
        self.assertEqual('https://api.mapbox.com/v4/directions/mapbox.walking/'
                         '50.032,40.54453;51.0345,41.2314.json?alternatives='
                         'false&instructions=text&geometry=false&steps=false&&'
                         'access_token=api_key',
                         self.wrapper.construct_request_string(),
                         'incorrect request string returned')

    # make_api_call tests
    @patch('MapboxAPIWrapper.requests.get')
    def test_call_api_calls_requests_get(self, mock_get):
        mock_response = mock.Mock()

        mock_response.json.return_value = self.expected_dict
        mock_get.return_value = mock_response

        url = 'https://api.mapbox.com/v4/directions/mapbox.walking/' \
              '50.032,40.54453;51.0345,41.2314.json?alternatives=' \
              'false&instructions=text&geometry=false&steps=false&&' \
              'access_token=api_key'

        response_dict = self.wrapper.call_api(request_url=url)
        mock_get.assert_called_once_with(url=url)
        mock_response.json.assert_called_once_with()
        self.assertEqual(response_dict, self.expected_dict)

    @patch('DataGeneration.MapboxAPIWrapper._handle_http_error')
    @patch('MapboxAPIWrapper.requests.get')
    def test_call_api_handles_http_error(self,
                                         mock_get, mock_http_error_handler):
        mock_response = mock.Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error

        mock_get.return_value = mock_response

        mock_http_error_handler.side_effect = CustomHTTPException()

        url = 'https://api.mapbox.com/v4/directions/mapbox.walking/' \
              '50.032,40.54453;51.0345,41.2314.json?alternatives=' \
              'false&instructions=text&geometry=false&steps=false&&' \
              'access_token=api_key'
        with self.assertRaises(CustomHTTPException):
            self.wrapper.call_api(request_url=url)

        mock_get.assert_called_once_with(url=url)
        self.assertEqual(1, mock_response.raise_for_status.call_count)

        self.assertEqual(0, mock_response.json.call_count)

        mock_http_error_handler.assert_called_once_with(http_error)

    # get_distance_from_api tests
    def test_get_distance_from_api_constructs_request_string(self):
        mock_construct = MagicMock(return_value='request_string')
        self.wrapper.construct_request_string = mock_construct
        mock_call = MagicMock(return_value=[])
        self.wrapper.call_api = mock_call

        self.wrapper.get_distance_from_api()
        mock_construct.assert_called_once_with()

    def test_get_distance_from_api_calls_make_api_call(self):
        mock_construct = MagicMock(return_value='request_string')
        self.wrapper.construct_request_string = mock_construct
        mock_call = MagicMock(return_value=[])
        self.wrapper.call_api = mock_call

        self.wrapper.get_distance_from_api()
        mock_call.assert_called_once_with('request_string')

    # parse_response tests
    def test_parse_response_returns_tuple(self):
        self.assertIsInstance(self.wrapper.parse_response(self.expected_dict),
                              tuple)

    def test_parse_response_returns_distance_value_in_first_element(self):
        parsed_response = self.wrapper.parse_response(self.expected_dict)
        self.assertEqual(221074, parsed_response[0])

    def test_parse_response_returns_duration_value_in_second_element(self):
        parsed_response = self.wrapper.parse_response(self.expected_dict)
        self.assertEqual(61045, parsed_response[1])
