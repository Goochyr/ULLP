#!/usr/bin/env python3
import yaml
import json
import os
from modules.core.screenControl import updateText, blankText, toggleBlanked
import modules.core.setlistHandler as sH

def init():
    global verses, currVerseNum, currVerse, currSlide, currSlideNum, order, orderMode, currSong, song, songlist, setlistName, blanked
    verses = {}
    currVerseNum = 0
    currVerse = ""
    currSlide = 0
    currSlideNum = 0
    order = []
    orderMode = True
    blanked = False
    song = json.load(open(os.getcwd()+"/songs/"+sH.songlist[0]+".json"))

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
    updateText(verses[currVerse][currSlide])

def blankSlide():
    blankText()

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
    global song
    if sH.currSong < len(sH.songlist)-1:
        sH.currSong += 1
        song = json.load(open(os.getcwd()+"/songs/"+sH.songlist[sH.currSong]+".json"))
        updateSong()
    else:
        toggleBlanked()

def prevSong():
    global song
    if sH.currSong > 0:
        sH.currSong -= 1
        song = json.load(open(os.getcwd()+"/songs/"+sH.songlist[sH.currSong]+".json"))
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
    charConvert = {"c": "c1", "v":"c2", "b":"b1", "n":"b2", "1":"v1", "2":"v2", "3":"v3", "p":"p1"}
    if char in charConvert and charConvert[char] in verses:
        currVerse = charConvert[char]
        currSlide = 0
        orderMode = False
        setSlide()

def goLive():
    setSlide()
