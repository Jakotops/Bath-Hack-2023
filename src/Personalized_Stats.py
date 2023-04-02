import json
from Live_Bus_Data import findETA
import requests

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


Total_Distance_Travelled(('-2.324970', '51.379060'), ('-2.34360', '51.379960'))
Total_Time_Spent_Travelling(('-2.324970', '51.379060'), ('-2.34360', '51.379960'))
