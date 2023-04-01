import requests


def find_bus_stop_data(bus_stop_id):
    url = f"https://www.firstbus.co.uk/api/get-next-bus?stop={bus_stop_id}"
    response = requests.get(url)
    bus_data = response.json()
    bus_stop_data = []
    for bus in bus_data["times"]:
        service = bus["ServiceNumber"]
        due = bus["Due"]
        bus_stop_data.append((service, due))

    return bus_stop_data