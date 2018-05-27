import csv
import shlex
import os
import modules.core.displaySong as dS
import modules.core.setlistHandler as sH
import modules.core.bibleHandler as bH
import modules.core.screenControl as sC

def init():
    global commandTable
    commandTable = {}

def buildCommandTable():
    global commandTable
    with open(os.getcwd()+"/modules/core/core.ullpref") as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            commandTable[row[0]] = [row[1], row[2], row[3]]
    print(commandTable)

def doCommand(incommand):
    global commandTable
    sendCommand=shlex.split(incommand)
    command = sendCommand[0]
    commandArgs = sendCommand[1:]
    print(commandArgs)
    returnString = ""
    if command in commandTable:
        if len(commandArgs) == int(commandTable[command][2]):
            module = globals()[commandTable[command][0]]
            result = getattr(module, str(commandTable[command][1]))(*commandArgs)
        else:
            returnString = "Wrong number of arguments"
    return returnString
