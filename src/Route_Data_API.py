import requests
import zipfile, io
url = "https://data.bus-data.dft.gov.uk/timetable/dataset/5813/download/"

headers = {
    'Authorization': 'Bearer 6ae6a620b33bf8bafe9b2f8f12326efcb8434206'
}

r = requests.get(url)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall("BUS_DATA")
