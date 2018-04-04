import os
import yaml
import json

def init():
    global songlist, searching, whichList, libSel, setSel, currSong, searchString
    searching = False
    searchString = ""
    songlist = []
    libSel = 0
    setSel = 0
    currSong = 0
    whichList = False

def fromConfig():
    global setlistName
    with open(os.path.join(os.getcwd(),"config.yml"), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    setlistName = cfg['setlist']
    getSaved(setlistName)

def getSaved(setlistName):
    global songlist
    setlist = json.load(open(os.getcwd()+"/setlists/"+setlistName+".json"))
    songlist = setlist['songs']

def refreshLib():
    global allsongs
    allsongs=os.listdir(os.getcwd()+"/songs/")
    allsongs.sort()

def addSong():
    global allsongs, libSel, songlist, whichList
    if not whichList:
        songlist.append(allsongs[libSel][:-5])

def nextItem():
    global whichList, setSel, libSel
    if whichList:
        if setSel < len(songlist)-1:
            setSel += 1
    else:
        if libSel < len(allsongs)-1:
            libSel += 1

def prevItem():
    global whichList, setSel, libSel
    if whichList:
        if setSel > 0:
            setSel -= 1
    else:
        if libSel > 0:
            libSel -= 1

def removeSong():
    global songlist, whichlist, setSel, currSong
    if whichList and len(songlist) > 0:
        del songlist[setSel]
        if setSel < currSong:
            currSong -= 1
        if setSel == len(songlist) and setSel > 0:
            setSel -=1

def switchList():
    global whichList
    if whichList:
        whichList = False
    else:
        whichList = True

def beginSearch():
    global searching, searchString
    searching = True
    searchString = ""

def endSearch():
    global searching
    searching = False

def addSearch(char):
    global searchString
    searchString += char
    songSearch()

def rmSearch():
    global searchString
    searchString = searchString[:-1]

def songSearch():
    global allsongs, searchString
    tempList = []
    for a in range(len(allsongs)):
        if searchString in allsongs[a]:
            tempList.append(allsongs[a])
    allsongs = tempList
    
