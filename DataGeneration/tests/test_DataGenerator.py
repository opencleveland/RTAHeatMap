from DataGeneration.DataGenerator import DataGenerator
import unittest


class test_DataGenerator(unittest.TestCase):

    def test_DataGenerator_exists(self):
        generator = DataGenerator()
        self.assertIsInstance(generator, DataGenerator)