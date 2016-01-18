import requests
from MapLocation import MapLocation
import os


class MapboxAPIWrapper:
    def __init__(self):
        pass

    def load_api_key_from_file(self, filename='api_key.txt'):
        if not os.path.exists(filename):
            raise ValueError("Could not find an api key file")
        with open(filename) as key_file:
            self.key = key_file.read()

    def set_origin_location(self, origin):
        if not isinstance(origin, MapLocation):
            raise TypeError('Origin Location must be a MapLocation object')
        self.origin = origin

    def set_destination_location(self, destination):
        if not isinstance(destination, MapLocation):
            raise TypeError('Destination Location must be a MapLocation object')
        self.destination = destination

    def construct_request_string(self):
        request_string = 'https://api.mapbox.com/v4/directions/mapbox.walking/'
        if not hasattr(self, 'origin'):
            raise UnboundLocalError('origin has not been specified')
        if not hasattr(self, 'destination'):
            raise UnboundLocalError('destination has not been specified')
        if not hasattr(self, 'key'):
            raise UnboundLocalError('key has not been specified')
        request_string += str(self.origin.latitude) + ','
        request_string += str(self.origin.longitude) + ';'
        request_string += str(self.destination.latitude) + ','
        request_string += str(self.destination.longitude)
        request_string += ('.json?alternatives=false&instructions=text&'
                           'geometry=false&steps=false&&access_token=')
        request_string += self.key
        return request_string

    def call_api(self, request_url):
        response = requests.get(url = request_url)
        return response.json()

    def get_distance_from_api(self):
        request_string = self.construct_request_string()
        return self.call_api(request_string)

    def parse_response(self, response_json):
        walking_distance = response_json['routes'][0]['distance']
        walking_duration = response_json['routes'][0]['duration']
        return (walking_distance, walking_duration)
