import requests
import zipfile, io
url = "https://data.bus-data.dft.gov.uk/timetable/dataset/5813/download/"

r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("BUS_DATA")
