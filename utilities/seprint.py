#!/usr/bin/env python3

# print selected data from a JSON file

import json
import sys

# get program arguments and options
try:
    inFile = open(sys.argv[1])
except:
    inFile = sys.stdin

# read the input
jsonStr = inFile.readline()
while jsonStr != "":
    inDict = json.loads(jsonStr)
    if inDict["inverters"] != {}:
        sys.stdout.write("Inverters\n")
        for inverter in sorted(inDict["inverters"].keys()):
            invDict = inDict["inverters"][inverter]
            sys.stdout.write(
                f"  {invDict['Date']} {invDict['Time']} {inverter}"
                f" Eday:{invDict['Eday']:9.2f}"
                f" Pac:{invDict['Pac']:7.2f}"
                f" Vac:{invDict['Vac']:6.2f}\n"
            )
    if inDict["optimizers"] != {}:
        sys.stdout.write("Optimizers\n")
        for optimizer in sorted(inDict["optimizers"].keys()):
            optDict = inDict["optimizers"][optimizer]
            sys.stdout.write(
                f"  {optDict['Date']} {optDict['Time']} {optimizer}"
                f" Eday:{optDict['Eday']:7.2f}\n"
            )
    if inDict["events"] != {}:
        sys.stdout.write("Events\n")
        for event in sorted(inDict["events"].keys()):
            eventDict = inDict["events"][event]
            sys.stdout.write(
                f"  {eventDict['Date']} {eventDict['Time']} {event}\n"
            )
    jsonStr = inFile.readline()
