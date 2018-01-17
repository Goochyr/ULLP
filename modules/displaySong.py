#!/usr/bin/env python3
import yaml
import json
import os
from modules.screenControl import updateText, blankText

def init():
    global verses, currVerseNum, currVerse, currSlide, currSlideNum, order, orderMode, currSong, song, songlist, setlistName, blanked
    verses = {}
    currVerseNum = 0
    currVerse = ""
    currSlide = 0
    currSlideNum = 0
    order = []
    orderMode = True
    currSong = 0
    blanked = False
    with open(os.path.join(os.getcwd(),"config.yml"), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    setlistName = cfg['setlist']
    setlist = json.load(open(os.getcwd()+"/setlists/"+setlistName+".json"))
    songlist = setlist['songs']
    song = json.load(open(os.getcwd()+"/songs/"+songlist[0]+".json"))

def updateSong():
    global song, verses, order, orderMode, currVerseNum, currVerse, currSlide
    verses = {}
    order = []
    orderMode = True
    for a in range(len(song["lyrics"])):
        verses[song["lyrics"][a]["id"]] = []
        for b in range(len(song["lyrics"][a]["slides"])):
            verses[song["lyrics"][a]["id"]].append(song["lyrics"][a]["slides"][b])
    for a in range(len(song["order"])):
        order.append(song["order"][a])
    currVerseNum = 0
    currVerse = order[currVerseNum]
    currSlide = 0

def setSlide():
    global blanked
    if not blanked:
        updateText(verses[currVerse][currSlide])

def blankSlide():
    blankText()

def toggleBlanked():
    global blanked
    if blanked:
        blanked = False
        setSlide()
    else:
        blanked = True
        blankSlide()

def nextSlide():
    global currSlide, currVerse, currVerseNum, orderMode
    if currSlide < len(verses[currVerse])-1:
        currSlide += 1
        setSlide()
    elif orderMode and currVerseNum < len(order)-1:
        currVerseNum += 1
        currVerse = order[currVerseNum]
        currSlide = 0
        setSlide()
    else:
        toggleBlanked()

def prevSlide():
    global currSlide, currVerse, currVerseNum, orderMode
    if currSlide > 0:
        currSlide -= 1
        setSlide()
    elif orderMode and currVerseNum > 0:
        currVerseNum -= 1
        currVerse = order[currVerseNum]
        currSlide = len(verses[currVerse])-1
        setSlide()
    else:
        toggleBlanked()

def restartSong():
    global currVerse, currVerseNum, currSlide, orderMode
    currVerseNum = 0
    currVerse = order[0]
    currSlide = 0
    orderMode = True
    setSlide()

def nextSong():
    global currSong, songlist, song
    if currSong < len(songlist)-1:
        currSong += 1
        song = json.load(open(os.getcwd()+"/songs/"+songlist[currSong]+".json"))
        updateSong()
    else:
        toggleBlanked()

def prevSong():
    global currSong, songlist, song
    if currSong > 0:
        currSong -= 1
        song = json.load(open(os.getcwd()+"/songs/"+songlist[currSong]+".json"))
        updateSong()
    else:
        toggleBlanked()

def updateSong():
    global song, verses, order, orderMode, currVerseNum, currVerse, currSlide
    verses = {}
    order = []
    orderMode = True
    for a in range(len(song["lyrics"])):
        verses[song["lyrics"][a]["id"]] = []
        for b in range(len(song["lyrics"][a]["slides"])):
            verses[song["lyrics"][a]["id"]].append(song["lyrics"][a]["slides"][b])
    for a in range(len(song["order"])):
        order.append(song["order"][a])
    currVerseNum = 0
    currVerse = order[currVerseNum]
    currSlide = 0
    setSlide()

def setVerse(char):
    global currVerse, currSlide, orderMode, verses
    charConvert = {"c": "c1", "v":"v1", "b":"b1", "1":"v1", "2":"v2", "3":"v3"}
    if char.char in charConvert and charConvert[char.char] in verses:
        currVerse = charConvert[char.char]
        currSlide = 0
        orderMode = False
        setSlide()

