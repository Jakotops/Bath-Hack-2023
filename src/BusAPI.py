import requests
import zipfile, io, xmltodict
import json
url = "https://data.bus-data.dft.gov.uk/timetable/dataset/5813/download/"

headers = {
    'Authorization': 'Bearer 6ae6a620b33bf8bafe9b2f8f12326efcb8434206'
    # replace 'your_access_token_here' with your actual access token
}

#response = requests.get(url, headers=headers)

r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("BUS_DATA")

with open("Routes/U1_U2-AVU1_AVU2--FBRI-BH-2023-04-09-W03_-_Wells-W03_-_Bath-BODS_V1_1.xml") as xml_file:
    U1 = xmltodict.parse(xml_file.read())

print(U1)
