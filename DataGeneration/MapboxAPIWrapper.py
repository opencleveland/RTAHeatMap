import requests
from DataGeneration.MapLocation import MapLocation
import os


class MapboxAPIWrapper:
    def __init__(self):
        self.key = ""

    def load_api_key_from_file(self, filename='api_key.txt'):
        if not os.path.exists(filename):
            raise ValueError("Could not find an api key file")
        with open(filename) as key_file:
            self.key = key_file.read()

    def get_distance_from_api(self, origin, destination):
        request_string = self.construct_request_string(origin, destination)
        return self.parse_response(self.call_api(request_string))

    def construct_request_string(self, origin, destination):
        request_string = 'https://api.mapbox.com/v4/directions/mapbox.walking/'
        if self.key == "":
            raise UnboundLocalError('key has not been specified')
        request_string += str(origin.latitude) + ','
        request_string += str(origin.longitude) + ';'
        request_string += str(destination.latitude) + ','
        request_string += str(destination.longitude)
        request_string += ('.json?alternatives=false&instructions=text&'
                           'geometry=false&steps=false&&access_token=')
        request_string += self.key
        return request_string

    def call_api(self, request_url, retries=3):
        while retries > 0:
            try:
                response = requests.get(url=request_url)
                try:
                    response.raise_for_status()
                    return response.json()
                except requests.exceptions.HTTPError as e:
                    self._handle_http_error(e)
            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout) as e:
                retries -= 1
                if not retries:
                    self._handle_connection_error(e)

    def parse_response(self, response_json):
        walking_distance = response_json['routes'][0]['distance']
        walking_duration = response_json['routes'][0]['duration']
        return walking_distance, walking_duration

    def _handle_http_error(self, e):
        pass

    def _handle_connection_error(self, e):
        pass
