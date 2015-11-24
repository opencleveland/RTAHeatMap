import unittest, os, errno, googlemaps, mock
from GoogleDistanceMatrixAPIWrapper import GoogleDistanceMatrixAPIWrapper

class TestGoogleDistanceMatrixAPIWrapper(unittest.TestCase):

    def test_google_api_wrapper_is_correct_type(self):
        self.assertIsInstance(GoogleDistanceMatrixAPIWrapper(),
                              GoogleDistanceMatrixAPIWrapper)

    # get_api_key_list tests
    def silent_remove(self, filename):
        try:
            os.remove(filename)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise

    # Create Dummy API Key File
    def create_dummy_api_key_file(self):
        with open('test_keys.txt', 'w') as key_file:
            key_file.writelines(['abc123\n', 'def456\n', 'ghi789\n'])

    # Deletes Dummy API Key File
    def delete_dummy_api_key_file(self):
        self.silent_remove('test_keys.txt')

    # Tests
    def test_get_api_key_list_returns_list(self):
        self.create_dummy_api_key_file()
        wrapper = GoogleDistanceMatrixAPIWrapper()
        keys = wrapper.get_api_key_list(filename = 'test_keys.txt')
        self.delete_dummy_api_key_file()

        self.assertIsInstance(keys, list)

    def test_get_api_key_list_raises_error_when_no_api_keys(self):
        self.assertRaises(ValueError,
                          GoogleDistanceMatrixAPIWrapper,
                          filename='3.txt')

    def test_get_api_key_list_returns_one_key(self):
        self.create_dummy_api_key_file()
        wrapper = GoogleDistanceMatrixAPIWrapper()
        keys = wrapper.get_api_key_list('test_keys.txt')
        self.delete_dummy_api_key_file()

        self.assertEqual(keys[0], 'abc123')

    def test_get_api_key_list_returns_three_key(self):
        self.create_dummy_api_key_file()
        wrapper = GoogleDistanceMatrixAPIWrapper()
        keys = wrapper.get_api_key_list('test_keys.txt')
        self.delete_dummy_api_key_file()

        self.assertEqual(keys[2], 'ghi789')
        self.assertEqual(len(keys), 3)

    #@mock.patch('GoogleDistanceMatrixAPIWrapper.googlemaps.Client')
    def test_create_googlemaps_connection_object(self):
        self.create_dummy_api_key_file()
        wrapper = GoogleDistanceMatrixAPIWrapper()

        wrapper.create_googlemaps_connection_object()
        self.delete_dummy_api_key_file()
        self.assertIsInstance(wrapper.gmaps, googlemaps.Client)

