import xmltodict

with open("BUS_DATA/U1_U2-AVU1_AVU2--FBRI-BH-2023-02-19-V46_-_Bath-V42_-_Wells-BODS_V1_1.xml") as xml_file:
    route = xmltodict.parse(xml_file.read())


def findTimetables(route):
    return