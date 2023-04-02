import json, os
from Live_Bus_Data import findETA
import requests

JSON_FILE_PATH = "StatsFolder"

class Stats():
    def __init__(self):
        json_files = self.find_files(JSON_FILE_PATH) #Stores names of json files in Questions folder
        self.json_list = []
        
        #Reads the json files and adds the objects to a list
        for file in json_files:
            self.json_list.append(self.read_json(f"{JSON_FILE_PATH}\{file}"))

        if len(self.json_list) == 0:
            #Raises error if there are no json files in the JSON_FILE_PATH directory
            raise Exception("Error: No json files could not be found")
        
    def find_files(self, folder_path):
        json_files = []
        try: 
            for path in os.listdir(folder_path):
            # check if current path is a file and its a json file
                if os.path.isfile(os.path.join(folder_path, path)) and ".json" in path:
                    json_files.append(path)
            return json_files
        except FileNotFoundError:
            #Raises exception if the specified directiory cannot be found
            raise FileNotFoundError(f"Cannot find json folder: {folder_path}")

    def read_json(self, file_path):
        with open(file_path, "r") as json_file:
            current_file = json.load(json_file)
        return current_file
    
    def get_all_json_files(self):
        return self.json_list[0]


def Total_Time_Spent_Travelling(init_bus_stop, end_bus_stop):
    response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?destinations="
                            + end_bus_stop[1] + ","
                            + end_bus_stop[0] + "&origins="
                            + init_bus_stop[1] + ","
                            + init_bus_stop[0] + "&units=imperial&key=AIzaSyBkslyyGinzvl6kxBYojdlXOege8u1lDf4")
    bus_data = response.json()
    time = bus_data["rows"][0]["elements"][0]["duration"]["value"]

    with open("Stats.json", "r") as infile:
        jsonr = json.load(infile)

    jsonr["total_time"] = jsonr["total_time"] + time
    with open("Stats.json", "w") as outfile:
        json.dump(jsonr, outfile)

def Total_Distance_Travelled(init_bus_stop, end_bus_stop):
    response = requests.get("https://maps.googleapis.com/maps/api/distancematrix/json?destinations="
                            +end_bus_stop[1]+","
                            +end_bus_stop[0]+"&origins="
                            +init_bus_stop[1]+","
                            +init_bus_stop[0]+"&units=imperial&key=AIzaSyBkslyyGinzvl6kxBYojdlXOege8u1lDf4")
    bus_data = response.json()
    distance = bus_data["rows"][0]["elements"][0]["distance"]["value"]

    with open("Stats.json", "r") as infile:
        jsonr = json.load(infile)

    jsonr["total_distance"] = jsonr["total_distance"] + distance
    with open("Stats.json", "w") as outfile:
        json.dump(jsonr, outfile)

def Accumulate_Trips():
    with open("Stats.json", "r") as infile:
        jsonr = json.load(infile)

    jsonr["accum_trips"] = jsonr["accum_trips"] + 1
    with open("Stats.json", "w") as outfile:
        json.dump(jsonr, outfile)

def Consecutive_Days():
    with open("Stats.json", "r") as infile:
        jsonr = json.load(infile)

    if jsonr["consecutive_days"] > 7:
        jsonr["consecutive_days"] = 1
    else:
        jsonr["consecutive_days"] = jsonr["consecutive_days"] + 1

    with open("Stats.json", "w") as outfile:
        json.dump(jsonr, outfile)

def Most_Frequent_Bus_On():
    with open("Stats.json", "r") as infile:
        jsonr = json.load(infile)

    jsonr["most_freq_bus_on"] = max(set(jsonr["most_freq_busOn"]), key=jsonr["most_freq_busOn"].count)

    with open("Stats.json", "w") as outfile:
        json.dump(jsonr, outfile)

def Most_Frequent_Bus_Off():
    with open("Stats.json", "r") as infile:
        jsonr = json.load(infile)

    jsonr["most_freq_bus_off"] = max(set(jsonr["most_freq_busOff"]), key=jsonr["most_freq_busOff"].count)

    with open("Stats.json", "w") as outfile:
        json.dump(jsonr, outfile)


#Total_Distance_Travelled(('-2.324970', '51.379060'), ('-2.34360', '51.379960'))
#Total_Time_Spent_Travelling(('-2.324970', '51.379060'), ('-2.34360', '51.379960'))

stat = Stats()
print(stat.get_all_json_files())