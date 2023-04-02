import requests


def find_bus_locations():
    #finds live locations of all buses in bath
    response = requests.get("https://bustimes.org/vehicles.json?ymax=51.417&xmax=-2.298&ymin=51.345&xmin=-2.424")
    bus_data = response.json()
    bus_locations = []
    for bus in bus_data:
        coordinates = bus["coordinates"]
        service = bus["service"]["line_name"]
        heading = bus["heading"]
        bus_locations.append((service, coordinates, heading))

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


def findETA(bus_location, bus_stop_location):
    # fetches driving time between 2 locations. locations in list format: [lat, long]
    try:
        start_lat = str(bus_location[1])
        start_long = str(bus_location[0])
        end_lat = str(bus_stop_location[1])
        end_long = str(bus_stop_location[0])
        response = requests.get(f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_lat}%2C{start_long}%3B{end_lat}%2C{end_long}?alternatives=false&geometries=geojson&overview=simplified&steps=false&access_token=pk.eyJ1Ijoiam0zMzIwIiwiYSI6ImNsZnlicWVoMzBmdW0zZW1tOHVuN3U1bngifQ.zOBybaJO3r99Ug4Cxpw55A")
        duration = response.json()["routes"][0]["duration"]
        return str(int(duration/60))+" mins"
    except:
        return "error estimating ETA"

print(find_bus_locations())

busCoord = find_bus_locations()[0][1]
print(type(busCoord[1]))
busCoord = [str(busCoord[1]), str(busCoord[0])]
print(busCoord)
stopCoord = ['51.378020', '-2.359030']
print(stopCoord)

print(findETA(busCoord, stopCoord))



