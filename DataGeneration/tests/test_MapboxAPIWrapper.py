import unittest
from mock import patch, mock_open, mock, Mock
import requests
from DataGeneration.MapboxAPIWrapper import MapboxAPIWrapper
from DataGeneration.MapLocation import MapLocation
from DataGeneration.MapboxAPIWrapper import MapboxAPIError


from sys import version_info
if version_info.major == 2:
    import __builtin__ as builtins
else:
    import builtins


class CustomHTTPException(Exception):
    pass


class CustomConnException(Exception):
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

    # constructor tests
    def test_map_api_wrapper_instantiates_empty_key(self):
        wrapper = MapboxAPIWrapper()
        self.assertEqual(wrapper.key, "")

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

    # _construct_request_string tests
    def test_construct_request_string_returns_string(self):
        self.wrapper.key = 'api_key'
        request_string = self.wrapper._construct_request_string(MapLocation(),
                                                               MapLocation())
        self.assertIsInstance(request_string, str)

    def test_constuct_request_string_errors_if_empty_key(self):
        with self.assertRaises(UnboundLocalError):
            self.wrapper._construct_request_string(MapLocation(),
                                                  MapLocation())

    def test_construct_request_string_produces_correct_output(self):
        origin = MapLocation(latitude=50.032, longitude=40.54453)
        destination = MapLocation(latitude=51.0345, longitude=41.2314)
        self.wrapper.key = 'api_key'
        self.assertEqual('https://api.mapbox.com/v4/directions/mapbox.walking/'
                         '40.54453,50.032;41.2314,51.0345.json?alternatives='
                         'false&instructions=text&geometry=false&steps=false&&'
                         'access_token=api_key',
                         self.wrapper._construct_request_string(origin,
                                                               destination),
                         'incorrect request string returned')

    def test_construct_request_string_can_use_driving_mode(self):
        origin = MapLocation(latitude=50.032, longitude=40.54453)
        destination = MapLocation(latitude=51.0345, longitude=41.2314)
        self.wrapper.key = 'api_key'
        self.assertEqual('https://api.mapbox.com/v4/directions/mapbox.driving/'
                         '40.54453,50.032;41.2314,51.0345.json?alternatives='
                         'false&instructions=text&geometry=false&steps=false&&'
                         'access_token=api_key',
                         self.wrapper._construct_request_string(origin,
                                                                destination,
                                                                mode='driving'),
                         'incorrect request string returned')


    # make_api_call tests
    @patch('MapboxAPIWrapper.requests.get')
    def test_call_api_calls_requests_get(self, mock_get):
        mock_response = Mock()

        mock_response.json.return_value = self.expected_dict
        mock_get.return_value = mock_response

        url = 'https://api.mapbox.com/v4/directions/mapbox.walking/' \
              '50.032,40.54453;51.0345,41.2314.json?alternatives=' \
              'false&instructions=text&geometry=false&steps=false&&' \
              'access_token=api_key'

        response_dict = self.wrapper._call_api(request_url=url)
        mock_get.assert_called_once_with(url=url)
        mock_response.json.assert_called_once_with()
        self.assertEqual(response_dict, self.expected_dict)

    @patch('DataGeneration.MapboxAPIWrapper._handle_http_error')
    @patch('MapboxAPIWrapper.requests.get')
    def test_call_api_handles_http_error(self,
                                         mock_get, mock_http_error_handler):
        mock_response = Mock()
        http_error = requests.exceptions.HTTPError()
        mock_response.raise_for_status.side_effect = http_error

        mock_get.return_value = mock_response

        mock_http_error_handler.side_effect = CustomHTTPException()

        url = 'https://api.mapbox.com/v4/directions/mapbox.walking/' \
              '50.032,40.54453;51.0345,41.2314.json?alternatives=' \
              'false&instructions=text&geometry=false&steps=false&&' \
              'access_token=api_key'
        with self.assertRaises(CustomHTTPException):
            self.wrapper._call_api(request_url=url)

        mock_get.assert_called_once_with(url=url)
        self.assertEqual(1, mock_response.raise_for_status.call_count)

        self.assertEqual(0, mock_response.json.call_count)

        mock_http_error_handler.assert_called_once_with(http_error)

    @mock.patch('DataGeneration.MapboxAPIWrapper._handle_connection_error')
    @mock.patch('MapboxAPIWrapper.requests.get')
    def test_call_api_connection_error(self, mock_get, mock_conn_error_handler):

        # Make the patched `requests.get` raise a connection error
        conn_error = requests.exceptions.ConnectionError()
        mock_get.side_effect = conn_error

        # Make the patched error handler raise a custom exception
        mock_conn_error_handler.side_effect = CustomConnException()

        url = 'https://api.mapbox.com/v4/directions/mapbox.walking/' \
              '50.032,40.54453;51.0345,41.2314.json?alternatives=' \
              'false&instructions=text&geometry=false&steps=false&&' \
              'access_token=api_key'
        with self.assertRaises(CustomConnException):
            self.wrapper._call_api(request_url=url)

        # Check that the function tried and failed to make 3 calls
        expected_calls = [mock.call(url=url)] * 3
        self.assertEqual(expected_calls, mock_get.call_args_list)

        # Make sure that the connection error handler is called
        mock_conn_error_handler.assert_called_once_with(conn_error)

    @mock.patch('MapboxAPIWrapper.requests.get')
    def test_get_connection_error_then_success(self, mock_get):

        # construct a response object for a successful call
        mock_response = Mock()
        mock_response.json.return_value = self.expected_dict

        # Make an instance of ConnectionError for the failure case
        conn_error = requests.exceptions.ConnectionError()

        # Give the patched get a list of side effects
        mock_get.side_effect = [conn_error, conn_error, mock_response]

        url = 'https://api.mapbox.com/v4/directions/mapbox.walking/' \
              '50.032,40.54453;51.0345,41.2314.json?alternatives=' \
              'false&instructions=text&geometry=false&steps=false&&' \
              'access_token=api_key'
        response_dict = self.wrapper._call_api(request_url=url)

        # Check that the function made the expected internal calls
        expected_calls = [mock.call(url=url)] * 3
        self.assertEqual(expected_calls, mock_get.call_args_list)
        self.assertEqual(1, mock_response.json.call_count)

        # Check the result
        self.assertEqual(response_dict, self.expected_dict)

    # get_distance_from_api tests
    def test_get_distance_from_api_constructs_request_string(self):
        self.wrapper._construct_request_string = Mock(return_value='request')
        self.wrapper._call_api = Mock(return_value=[])
        self.wrapper._parse_response = Mock()

        origin = MapLocation(1, 1, 1)
        destination = MapLocation(2, 2, 2)

        self.wrapper.get_distance_from_api(origin, destination)
        self.wrapper._construct_request_string.\
            assert_called_once_with(origin, destination, 'walking')

    def test_get_distance_from_api_passes_in_mode_string(self):
        self.wrapper._construct_request_string = Mock(return_value='request')
        self.wrapper._call_api = Mock(return_value=[])
        self.wrapper._parse_response = Mock()

        origin = MapLocation(1, 1, 1)
        destination = MapLocation(2, 2, 2)

        self.wrapper.get_distance_from_api(origin, destination, mode='driving')
        self.wrapper._construct_request_string. \
            assert_called_once_with(origin, destination, 'driving')

    def test_get_distance_from_api_calls_make_api_call(self):
        self.wrapper._construct_request_string = Mock(return_value='request')
        self.wrapper._call_api = Mock(return_value=[])
        self.wrapper._parse_response = Mock()

        self.wrapper.get_distance_from_api(MapLocation(), MapLocation())
        self.wrapper._call_api.assert_called_once_with('request')

    def test_get_distance_from_api_parses_response(self):
        self.wrapper._construct_request_string = Mock()
        self.wrapper._call_api = Mock(return_value="json")
        self.wrapper._parse_response = Mock(return_value=[5, 10])

        dist = self.wrapper.get_distance_from_api(MapLocation(), MapLocation())
        self.wrapper._parse_response.assert_called_once_with("json")
        self.assertEqual([5, 10], dist)


    # _parse_response tests
    def test_parse_response_returns_tuple(self):
        self.assertIsInstance(self.wrapper._parse_response(self.expected_dict),
                              dict)

    def test_parse_response_returns_distance_value_in_first_element(self):
        parsed_response = self.wrapper._parse_response(self.expected_dict)
        self.assertEqual(221074, parsed_response["distance"])

    def test_parse_response_returns_duration_value_in_second_element(self):
        parsed_response = self.wrapper._parse_response(self.expected_dict)
        self.assertEqual(61045, parsed_response["time"])

    # error tests
    def test_handle_http_error_raises_MapboxAPIError(self):
        with self.assertRaises(MapboxAPIError):
            self.wrapper._handle_http_error(Exception())

    def test_handle_connection_error_raises_MapboxAPIError(self):
        with self.assertRaises(MapboxAPIError):
            self.wrapper._handle_connection_error(Exception())
