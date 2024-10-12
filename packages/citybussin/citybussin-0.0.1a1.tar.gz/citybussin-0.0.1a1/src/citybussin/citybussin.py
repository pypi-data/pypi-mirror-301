import requests

class Citybussin:
    BASE_URL = "https://bus.gocitybus.com/RouteMap"

    def _get_base_data(self):
        api_url = f"{self.BASE_URL}/GetBaseData/"
        r = requests.post(api_url)
        return r.json()

    def _get_pattern_paths(self, route_key):
        api_url = f"{self.BASE_URL}/GetPatternPaths/"
        payload = {"routeKeys[]": route_key}
        r = requests.post(api_url, data=payload)
        return r.json()

    def _get_next_depart_times(self, route_key, direction_key, stop_code):
        api_url = f"{self.BASE_URL}/GetNextDepartTimes/"
        payload = {
            "routeDirectionKeys[0][routeKey]": route_key,
            "routeDirectionKeys[0][directionKey]": direction_key,
            "stopCode": stop_code
        }
        r = requests.post(api_url, data=payload)
        return r.json()

    def _get_vehicles(self, route_key):
        api_url = f"{self.BASE_URL}/GetVehicles/"
        payload = {"routeKeys[]": route_key}
        r = requests.post(api_url, data=payload)
        return r.json()


    def get_bus_routes(self):
        return self._get_base_data()["routes"]

    def get_service_interruptions(self):
        return self._get_base_data()["serviceInterruptions"]

    def get_pattern_paths(self, route_key):
        return self._get_pattern_paths(route_key)[0]["patternPaths"]

    def get_vehicles_by_directions(self, route_key):
        return self._get_pattern_paths(route_key)["vehiclesByDirections"]

    def get_route_direction_times(self, route_key, direction_key, stop_code):
        return self._get_next_depart_times(route_key, direction_key, stop_code)["routeDirectionTimes"]

    def get_vehicles(self, route_key):
        return self._get_vehicles(route_key)["vehiclesByDirections"]

    def get_route_by_short_name(self, short_name):
        for route in self.get_bus_routes():
            if route["shortName"] == short_name:
                return route
        return None

    def get_route_by_key(self, route_key):
        for route in self.get_bus_routes():
            if route["key"] == route_key:
                return route
        return None

    def get_route_directions(self, route_key):
        for route in self.get_bus_routes():
            if route["key"] == route_key:
                return route["directionList"]

    def get_route_stops(self, route_key):
        stops = []

        for pattern_path in self.get_pattern_paths(route_key):
            for pattern_point in pattern_path["patternPoints"]:
                if "stop" in pattern_point and pattern_point["stop"] is not None:
                    stops.append(pattern_point["stop"])
        return stops

    def get_next_depart_times(self, route_key, direction_key, stop_code):
        return self._get_next_depart_times(route_key, direction_key, stop_code)["routeDirectionTimes"][0]["nextDeparts"]


def main():
    c = Citybussin()


if __name__ == "__main__":
    main()