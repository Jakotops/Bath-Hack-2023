import xmltodict

def getroute():
    with open("BUS_DATA/U1_U2-AVU1_AVU2--FBRI-BH-2023-02-19-V46_-_Bath-V42_-_Wells-BODS_V1_1.xml") as xml_file:
        route = xmltodict.parse(xml_file.read())
    return route

def findBusStops():
    route = getroute()
    #returns list of bus stops on route, name and id
    return route["TransXChange"]["StopPoints"]["AnnotatedStopPointRef"]


def findBusStopCoordinates(bus_id):
    routes = getroute()
    # returns list of coordinates for the bus stops
    coordinates = []
    route = routes["TransXChange"]["RouteSections"]["RouteSection"][bus_id]["RouteLink"]
    for bus_stop in route:
        points = bus_stop["Track"]["Mapping"]["Location"]
        coordinates.append((points[0]["Latitude"], points[0]["Longitude"]))
    return coordinates


def findRouteCoordinatesList(bus_id):
    #returns list of coordinates for entire bus route
    routes = getroute()
    coordinates = []
    route = routes["TransXChange"]["RouteSections"]["RouteSection"][bus_id]["RouteLink"]
    for bus_stop in route:
        points = bus_stop["Track"]["Mapping"]["Location"]
        for coordinate in points:
            coordinates.append((float(coordinate["Latitude"]), float(coordinate["Longitude"])))
    return coordinates

print(findBusStops())