import unittest
from UniformMapGenerator import UniformMapGenerator
import pandas


class TestUniformMapGenerator(unittest.TestCase):
    # get_number_of_intervals tests
    def test_get_number_of_intervals_returns_int(self):
        generator = UniformMapGenerator()
        self.assertIsInstance(generator.get_number_of_intervals(1, 1, 1),
                              int)

    def test_get_number_of_intervals_integers(self):
        generator = UniformMapGenerator()
        number_of_intervals = generator.get_number_of_intervals(3, 10, 1)
        self.assertEqual(number_of_intervals, 8)

    def test_get_number_of_intervals_decimal_resolution(self):
        generator = UniformMapGenerator()
        number_of_intervals = generator.get_number_of_intervals(2, 3, 0.3)
        self.assertEqual(number_of_intervals, 5)

    def test_get_number_of_intervals_decimal_properties(self):
        generator = UniformMapGenerator()
        number_of_intervals = generator.get_number_of_intervals(2, 3, 0.3)
        self.assertEqual(number_of_intervals, 5)

    # instantiate_output_dataframe tests
    def test_empty_output_dataframe_is_pandas_dataframe(self):
        generator = UniformMapGenerator()
        self.assertIsInstance(generator.instantiate_output_dataframe(1),
                              pandas.DataFrame)

    def test_empty_output_dataframe_is_correct_length(self):
        generator = UniformMapGenerator()
        dataframe = generator.instantiate_output_dataframe(20)
        self.assertEqual(len(dataframe), 20)

    def test_empty_out_dataframe_has_correct_column_names(self):
        generator = UniformMapGenerator()
        dataframe = generator.instantiate_output_dataframe(20)
        self.assertEqual(dataframe.columns[0], 'addr_lat')
        self.assertEqual(dataframe.columns[1], 'addr_lon')

    # GetUniformCoordinateMap tests
    def test_GetUniformCoordinateMap_returns_pandas_dataframe(self):
        generator = UniformMapGenerator()
        dataframe = generator.get_uniform_coordinate_map(1, 1, 1, 1, 1, 1)
        self.assertIsInstance(dataframe, pandas.DataFrame)

    def test_getUniformCoordinateMap_output_is_expected_length(self):
        generator = UniformMapGenerator()
        dataframe = generator.get_uniform_coordinate_map(1, 10,
                                                         6, 20,
                                                         1, 1)
        self.assertEqual(len(dataframe), 150, "Output length should be 150")