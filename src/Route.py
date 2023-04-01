with open("BUS_DATA/U1_U2-AVU1_AVU2--FBRI-BH-2023-04-09-W03_-_Wells-W03_-_Bath-BODS_V1_1.xml") as xml_file:
    route = xmltodict.parse(xml_file.read())

def findBusStops(route):
    #returns list of bus stops on route, name and id
    return route["TransXChange"]["StopPoints"]["AnnotatedStopPointRef"]

def findBusStopCoordinates(route):
    # returns list of coordinates for the bus stops
    coordinates = []
    route1 = route["TransXChange"]["RouteSections"]["RouteSection"][0]["RouteLink"]
    for bus_stop in route1:
        points = bus_stop["Track"]["Mapping"]["Location"]
        coordinates.append((points[0]["Longitude"], points[0]["Latitude"]))
    return coordinates

def findRouteCoordinatesList(route):
    #returns list of coordinates for entire bus route
    coordinates = []
    route1 = route["TransXChange"]["RouteSections"]["RouteSection"][0]["RouteLink"]
    for bus_stop in route1:
        points = bus_stop["Track"]["Mapping"]["Location"]
        for coordinate in points:
            coordinates.append((coordinate["Longitude"], coordinate["Latitude"]))
    return coordinates


findBusStops(route)
findRouteCoordinatesList(route)
findBusStopCoordinates(route)