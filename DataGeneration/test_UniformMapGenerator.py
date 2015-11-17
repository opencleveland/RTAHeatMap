import unittest
from GenerateUniformAddresses import UniformMapGenerator


class TestUniformMapGenerator(unittest.TestCase):
    def test_get_number_of_intervals_returns_int(self):
        map_generator = UniformMapGenerator()
        self.assertIsInstance(map_generator.get_number_of_intervals(1, 1, 1),
                              int)

    def test_get_number_of_intervals_integers(self):
        map_generator = UniformMapGenerator()
        number_of_intervals = map_generator.get_number_of_intervals(3, 10, 1)
        self.assertEqual(number_of_intervals, 8)

    def test_get_number_of_intervals_decimal_resolution(self):
        map_generator = UniformMapGenerator()
        number_of_intervals = map_generator.get_number_of_intervals(2, 3, 0.3)
        self.assertEqual(number_of_intervals, 5)

    def test_get_number_of_intervals_decimal_properties(self):
        map_generator = UniformMapGenerator()
        number_of_intervals = map_generator.get_number_of_intervals(2, 3, 0.3)
        self.assertEqual(number_of_intervals, 5)