import xmltodict

with open("BUS_DATA/U1_U2-AVU1_AVU2--FBRI-BH-2023-04-09-W03_-_Wells-W03_-_Bath-BODS_V1_1.xml") as xml_file:
    route = xmltodict.parse(xml_file.read())


def findTimetables(route):
    return