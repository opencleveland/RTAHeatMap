import os
import googlemaps


class GoogleDistanceMatrixAPIWrapper():

    def __init__(self,
                 filename = 'api_keys.txt'):
        self.key_list = self.get_api_key_list(filename)

    def get_api_key_list(self,
                         filename = 'api_keys.txt'):
        if not os.path.exists(filename):
            raise ValueError('Invalid API key source file')
        with open(filename, 'r') as key_file:
            output_list = (key_file.read().splitlines())
        return output_list

    def create_googlemaps_connection_object(self):
        self.gmaps = googlemaps.Client(key = self.key_list[0])

