import unittest, mock
from mock import patch, mock_open
from MapboxAPIWrapper import MapboxAPIWrapper

from sys import version_info
if version_info.major == 2:
    import __builtin__ as builtins
else:
    import builtins

class TestMapboxAPIWrapper(unittest.TestCase):

    def test_mapbox_api_wrapper_class_exists(self):
        wrapper = MapboxAPIWrapper()
        self.assertTrue(True)

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


