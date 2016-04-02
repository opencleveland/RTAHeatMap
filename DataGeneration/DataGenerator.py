from DataGeneration import DatabaseHandler
from MapboxAPIWrapper import MapboxAPIWrapper
from MapboxAPIWrapper import MapboxAPIError
import math
import requests


class DataGenerator:

    def __init__(self,
                 handler=DatabaseHandler(db_file_name='db.sqlite3'),
                 stops=None,
                 wrapper=None):
        self.handler = handler
        if stops is None:
            stops = handler.get_all_stops()
        else:
            self.stops = stops
        if wrapper is None:
            self.wrapper = self._get_api_wrapper('api_key.txt')
        else:
            self.wrapper = wrapper

    def initialize(self, db='db.sqlite3', api_key='api_key.txt'):
        """
        Initializes the DataGenerator. Connects to the database, collects all
        stops from the database, and initializes the API wrapper.

        Args:
            db (str): File path to the sqlite3 database.
            api_key (str): File path to a text file containing an API key.
        """
        self.handler = self._get_database_handler(db)
        self.stops = self.handler.get_all_stops()
        self.wrapper = self._get_api_wrapper(api_key)

    def begin(self, stops_per_address=5, verbose=True, mode='walking'):
        """
        Begins collection of distances to closest stops from each address.
        Stores each address-stop pair and associated walking distance and time
        in the routes table of the database.

        Args:
            stops_per_address (int): Number of stops per address used to query
                the api for walking distance. The stops selected are the closest
                stops to the address by straight line distance. Default value is
                5.
            verbose (bool): If True (default), displays status information
                during data collection.
            mode (str): Mode of travel to query against the api. Options are:
                'walking' (default) - Walking on foot
                'driving' - Driving by car
                'cycling' - Cycling by bicycle
        """
        address_generator = self.handler.get_address_generator(verbose=verbose)
        for address in address_generator:
            if verbose:
                print('processing address: {}, {}, id: {}'.
                      format(address.latitude, address.longitude, address.id))
            closest_stops = self._get_closest_locations(address,
                                                        self.stops,
                                                        n=stops_per_address)
            for stop in closest_stops:
                try:
                    self.process_stop(address, stop, verbose, mode)
                except requests.exceptions.RequestException as e:
                    print('error processing stop: {}'.format(e.message))
                    continue

    def process_stop(self, address, stop, verbose, mode='walking'):
        if verbose:
            print('processing stop: {}, {}, id: {}'.
                  format(stop.latitude, stop.longitude, stop.id))
        result = self.wrapper.get_distance_from_api(address, stop, mode)
        if verbose:
            print('distance: {}, time: {}'.format(result["distance"],
                                                  result["time"]))
        self.handler.add_route(address.id,
                               stop.id,
                               result["distance"],
                               result["time"])

    def _get_database_handler(self, db_file_name='db.sqlite3'):
        handler = DatabaseHandler(db_file_name)
        return handler

    def _get_api_wrapper(self, api_key_file='api_key.txt'):
        wrapper = MapboxAPIWrapper()
        wrapper.load_api_key_from_file(api_key_file)
        return wrapper

    def _get_closest_locations(self, source, destinations, n):
        location_list = []
        for destination in destinations:
            distance = math.sqrt((source.latitude - destination.latitude)**2 +
                                 (source.longitude - destination.longitude)**2)
            location_list.append((distance, destination))
        return [loc[1] for loc in sorted(location_list)[0:n]]
