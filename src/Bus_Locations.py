import requests


def find_bus_locations():
    response = requests.get("https://bustimes.org/vehicles.json?ymax=51.417&xmax=-2.298&ymin=51.345&xmin=-2.424")
    bus_data = response.json()
    bus_locations = []
    for bus in bus_data:
        coordinates = bus["coordinates"]
        service = bus["service"]["line_name"]
        bus_locations.append((service, coordinates))

    return bus_locations


