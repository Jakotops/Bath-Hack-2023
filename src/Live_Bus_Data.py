import requests


def find_bus_locations():
    #finds live locations of all buses in bath
    response = requests.get("https://bustimes.org/vehicles.json?ymax=51.417&xmax=-2.298&ymin=51.345&xmin=-2.424")
    bus_data = response.json()
    bus_locations = []
    for bus in bus_data:
        coordinates = bus["coordinates"]
        service = bus["service"]["line_name"]
        bus_locations.append((service, coordinates))

    return bus_locations


def find_bus_stop_data(bus_stop_id):
    #finds next expected buses for a bus stop
    url = f"https://www.firstbus.co.uk/api/get-next-bus?stop={bus_stop_id}"
    response = requests.get(url)
    bus_data = response.json()
    bus_stop_data = []
    for bus in bus_data["times"]:
        service = bus["ServiceNumber"]
        due = bus["Due"]
        bus_stop_data.append((service, due))

    return bus_stop_data



