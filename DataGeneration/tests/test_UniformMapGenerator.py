import unittest

import pandas

from RTAHeatMap.DataGeneration.UniformMapGenerator import UniformMapGenerator


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
        self.assertEqual(dataframe.columns[0], 'latitude')
        self.assertEqual(dataframe.columns[1], 'longitude')

    # get_next_coordinate tests
    def test_get_next_coordinate_first_two(self):
        map_generator = UniformMapGenerator()
        coordinate_gen = map_generator.get_next_coordinate(0.5, 5, 0.2)
        self.assertEqual(coordinate_gen.next(), 0.5)
        self.assertEqual(coordinate_gen.next(), 0.7)

    def test_get_next_coordinate_last_coordinate_includes_end(self):
        map_generator = UniformMapGenerator()
        coordinate_gen = map_generator.get_next_coordinate(0.9, 1, 0.2)
        self.assertEqual(coordinate_gen.next(), 0.9)
        self.assertEqual(coordinate_gen.next(), 1.1)
        self.assertRaises(StopIteration, coordinate_gen.next)

    def test_get_next_coordinate_last_coordinate_doesnt_overshoot(self):
        map_generator = UniformMapGenerator()
        coordinate_gen = map_generator.get_next_coordinate(0.8, 1, 0.2)
        self.assertEqual(coordinate_gen.next(), 0.8)
        self.assertEqual(coordinate_gen.next(), 1)
        self.assertRaises(StopIteration, coordinate_gen.next)

    # get_uniform_coordinate_map tests
    def test_get_uniform_coordinate_map_returns_pandas_dataframe(self):
        generator = UniformMapGenerator()
        dataframe = generator.get_uniform_coordinate_map(1, 1, 1, 1, 1, 1)
        self.assertIsInstance(dataframe, pandas.DataFrame)

    def test_get_uniform_coordinate_map_output_is_expected_length(self):
        generator = UniformMapGenerator()
        dataframe = generator.get_uniform_coordinate_map(1, 10,
                                                         6, 20,
                                                         1, 1)
        self.assertEqual(len(dataframe), 150, "Output length should be 150")

    def test_get_uniform_map_simple_latitude_is_correct(self):
        generator = UniformMapGenerator()
        df = generator.get_uniform_coordinate_map(1, 2, 1, 2, 1, 1)
        self.assertEqual(1, df.iloc[0, 0])
        self.assertEqual(1, df.iloc[1, 0])
        self.assertEqual(2, df.iloc[2, 0])
        self.assertEqual(2, df.iloc[3, 0])

    def test_get_uniform_map_simple_longitude_is_correct(self):
        generator = UniformMapGenerator()
        df = generator.get_uniform_coordinate_map(1, 2, 1, 2, 1, 1)
        self.assertEqual(1, df.iloc[0, 1])
        self.assertEqual(2, df.iloc[1, 1])
        self.assertEqual(1, df.iloc[2, 1])
        self.assertEqual(2, df.iloc[3, 1])
