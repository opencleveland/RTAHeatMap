from DataGeneration import DataGenerator
from DataGeneration import DatabaseHandler
from DataGeneration import MapLocation
import unittest
from mock import Mock, patch

class test_DataGenerator(unittest.TestCase):

    # __init__ tests
    def test_constructor_sets_stops_array_to_empty_list(self):
        generator = DataGenerator()
        self.assertEqual([], generator.stops)

    # initialize tests
    @patch('DataGeneration.DataGenerator.get_database_handler')
    def test_DataGenerator_exists(self,
                                  mock_get_db):
        generator = DataGenerator()
        self.assertIsInstance(generator, DataGenerator)

    @patch('DataGeneration.DatabaseHandler.get_all_stops')
    @patch('DataGeneration.DataGenerator.get_database_handler')
    def test_start_initializes_database(self,
                                        mock_get_db,
                                        mock_get_all_stops):
        generator = DataGenerator()
        mock_get_db.return_value = DatabaseHandler(full=False)
        generator.initialize()
        mock_get_db.assert_called_once_with()

    @patch('DataGeneration.DatabaseHandler.get_all_stops')
    @patch('DataGeneration.DataGenerator.get_database_handler')
    def test_start_pulls_all_stops(self,
                                   mock_get_db,
                                   mock_get_all_stops):
        generator = DataGenerator()
        mock_get_db.return_value = DatabaseHandler(full=False)
        generator.initialize()
        mock_get_all_stops.assert_called_once_with()

    # get_database_handler tests
    def test_get_database_handler_returns_DatabaseHandler(self):
        generator = DataGenerator()
        self.assertIsInstance(generator.get_database_handler(), DatabaseHandler)
