class MapLocation:
    def __init__(self, latitude = 0, longitude = 0):
        if latitude > 90 or latitude < -90:
            raise ValueError("latitude must be between -90 and 90")
        if longitude > 180 or longitude < -180:
            raise ValueError("longitude must be between -180 and 180")
        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other):
        return self.latitude == other.latitude and \
               self.longitude == other.longitude

    def __str__(self):
        return "{}, {}".format(self.latitude, self.longitude)
