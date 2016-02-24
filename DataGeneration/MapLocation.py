class MapLocation:
    def __init__(self, latitude=0, longitude=0, id=0):
        if latitude > 90 or latitude < -90:
            raise ValueError("latitude must be between -90 and 90")
        if longitude > 180 or longitude < -180:
            raise ValueError("longitude must be between -180 and 180")
        self.latitude = latitude
        self.longitude = longitude
        self.id = id

    def __eq__(self, other):
        return self.latitude == other.latitude and \
               self.longitude == other.longitude and \
               self.id == other.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if self.latitude == other.latitude and self.longitude == other.latitude:
            return self.id < other.id
        elif self.latitude == other.latitude:
            return self.longitude < other.longitude
        else:
            return self.latitude < other.latitude

    def __str__(self):
        return "{}, {}".format(self.latitude, self.longitude)
