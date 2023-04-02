import json
from Live_Bus_Data import findETA

def Total_Time_Spent_Travelling(init_pos, end_pos):
    time = findETA(init_pos, end_pos)

    with open("Stats.json", "r") as infile:
        jsonr = json.load(infile)

    jsonr["total_time"] = jsonr["total_time"] + time
    with open("Stats.json", "w") as outfile:
        json.dump(jsonr, outfile)

def Total_Distance_Travelled(init_pos, end_pos):
    distance = 0

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
    stop = ""
    return stop

def Most_Frequent_Bus_Off():
    stop = ""
    return stop
