from DataGeneration import DataGenerator
from DataGeneration import DatabaseHandler
import unittest
from mock import Mock, patch

class test_DataGenerator(unittest.TestCase):

    @patch('DataGeneration.DataGenerator.get_database_handler')
    def test_DataGenerator_exists(self,
                                  mock_get_db):
        generator = DataGenerator()
        self.assertIsInstance(generator, DataGenerator)

    @patch('DataGeneration.DataGenerator.get_database_handler')
    def test_begin_initializes_database(self,
                                        mock_get_db):
        generator = DataGenerator()
        generator.start()
        mock_get_db.assert_called_once_with()

    # get_database_handler tests
    def test_get_database_handler_returns_DatabaseHandler(self):
        generator = DataGenerator()
        self.assertIsInstance(generator.get_database_handler(), DatabaseHandler)
