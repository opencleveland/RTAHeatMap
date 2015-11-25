from urllib2 import Request, urlopen, URLError
import os

class MapboxAPIWrapper:
    def __init__(self):
        pass

    def load_api_key_from_file(self, filename='api_key.txt'):
        if not os.path.exists(filename):
            raise ValueError("Could not find an api key file")
        with open(filename) as key_file:
            self.key = key_file.read()