import unittest
from DataGeneration.MapLocation import MapLocation

class TestMapLocation(unittest.TestCase):

    def test_MapLocation_class_exists(self):
        location = MapLocation()
        self.assertIsInstance(location, MapLocation)

    def test_constructor_instantiates_latitude_zero_as_default(self):
        location = MapLocation()
        self.assertEquals(0, location.latitude)

    def test_constructor_instantiates_longitude_zero_as_default(self):
        location = MapLocation()
        self.assertEqual(0, location.longitude)

    def test_constructor_allows_normal_latitude_setting(self):
        location = MapLocation(latitude = 75)
        self.assertEqual(75, location.latitude)

    def test_constructor_allows_normal_longitude_setting(self):
        location = MapLocation(longitude = 120)
        self.assertEqual(120, location.longitude)

    def test_constructor_errors_for_too_large_latitude(self):
        self.assertRaises(ValueError, MapLocation, 90.001)

    def test_constructor_errors_for_too_small_latitude(self):
        self.assertRaises(ValueError, MapLocation, -90.001)

    def test_constructor_errors_for_too_large_longitude(self):
        self.assertRaises(ValueError, MapLocation, 0, 180.001)

    def test_constructor_errors_for_too_small_longitude(self):
        self.assertRaises(ValueError, MapLocation, 0, -180.001)