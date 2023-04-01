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


def find_bus_stop_data(bus_stop):
    url = f"http://first.transportapi.com/v3/uk/bus/stop_timetables/{bus_stop}.json?app_id=75da7e19&app_key=8a756a1369a55907a33042def6008ec8&group=false&limit=20&live=true"
    response = requests.get(url)
    bus_data = response.json()
    bus_stop_data = []
    for bus in bus_data["departures"]["all"]:
        service = bus["line"]
        due = bus["expected"]["arrival"]["time"]
        try:
            occupied_seats = bus["status"]["occupancy"]["types"][0]["occupied"]
            total_seats = bus["status"]["occupancy"]["types"][0]["capacity"]
        except:
            occupied_seats = 0
            total_seats = 0
        bus_stop_data.append((service, due, occupied_seats, total_seats))
    return bus_stop_data




def findETA(bus_location, bus_stop_location):
    # fetches driving time between 2 locations. locations in list format: [lat, long]
    start_lat = str(bus_location[0])
    start_long = str(bus_location[1])
    end_lat = str(bus_stop_location[0])
    end_long = str(bus_stop_location[1])
    response = requests.get(f"https://api.mapbox.com/directions/v5/mapbox/driving/{start_lat}%2C{start_long}%3B{end_lat}%2C{end_long}?alternatives=false&geometries=geojson&overview=simplified&steps=false&access_token=pk.eyJ1Ijoiam0zMzIwIiwiYSI6ImNsZnlicWVoMzBmdW0zZW1tOHVuN3U1bngifQ.zOBybaJO3r99Ug4Cxpw55A")
    duration = response.json()["routes"][0]["duration"]
    return str(int(duration/60))+" mins"


print(findOccupancy("0180BAC30035"))