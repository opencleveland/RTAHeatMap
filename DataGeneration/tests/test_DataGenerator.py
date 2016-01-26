from DataGeneration.DataGenerator import DataGenerator
from DataGeneration.DatabaseHandler import DatabaseHandler
import unittest
from mock import Mock

class test_DataGenerator(unittest.TestCase):

    def test_DataGenerator_exists(self):
        generator = DataGenerator()
        self.assertIsInstance(generator, DataGenerator)

    def test_begin_initializes_database(self):
        generator = DataGenerator()
        mock_get_database_handler = Mock()
        generator.get_database_handler = mock_get_database_handler
        generator.start()
        mock_get_database_handler.assert_called_once_with()

    # get_database_handler tests
    def test_get_database_handler_returns_DatabaseHandler(self):
        generator = DataGenerator()
        self.assertIsInstance(generator.get_database_handler(), DatabaseHandler)
