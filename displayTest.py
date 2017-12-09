#!/usr/bin/env python3
from tkinter import *
import json
import yaml
import os
import PIL
from PIL import ImageTk, Image

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)
themeName = cfg['theme']
setlistName = cfg['setlist']
with open(os.getcwd()+"/themes/"+themeName+".yml") as ymlfile1:
    theme = yaml.load(ymlfile1)
setlist = json.load(open(os.getcwd()+"/setlists/"+setlistName+".json"))
songlist = setlist['songs']
song = json.load(open(os.getcwd()+"/songs/"+songlist[0]+".json"))

verses = {}
currVerseNum = 0
currVerse = ""
currSlide = 0
order = []
orderMode = True
currSong = 0

root = Tk()
rootHeight = root.winfo_screenheight()
rootWidth = root.winfo_screenwidth()

textFrame = Frame(root, width=rootWidth, height=rootHeight*0.75)
mainText = Text(textFrame, bg=theme['bgColour'], borderwidth=0)
logoBox = Frame(root, width=rootWidth, height=rootHeight*0.25)
leftLogo = Label(logoBox, border=0, background='black')
rightLogo = Label(logoBox, border=0, background='black')

if theme['leftImg'] != 'none':
    leftImgPath = os.getcwd()+"/logos/"+theme['leftImg']+".png"
    leftImg0 = Image.open(leftImgPath)
    [limageSizeWidth, limageSizeHeight] = leftImg0.size
    leftRatio = (rootHeight*0.25)/limageSizeHeight
    leftImg0 = leftImg0.resize((int(leftRatio*limageSizeWidth), int(leftRatio*limageSizeHeight)), Image.ANTIALIAS)
    leftImg = PIL.ImageTk.PhotoImage(leftImg0)
    leftLogo.config(image=leftImg)

if theme['rightImg'] != 'none':
    rightImgPath = "revologo.jpg"
    rightImg0 = Image.open(rightImgPath)
    [rimageSizeWidth, rimageSizeHeight] = rightImg0.size
    rightRatio = (rootHeight*0.25)/rimageSizeHeight
    rightImg0 = rightImg0.resize((int(rightRatio*rimageSizeWidth), int(rightRatio*rimageSizeHeight)), Image.ANTIALIAS)
    rightImg = PIL.ImageTk.PhotoImage(rightImg0)
    rightLogo.config(image=rightImg)

def setVerse(char):
    global currVerse, currSlide, orderMode, verses
    charConvert = {"c": "c1", "v":"v1", "b":"b1", "1":"v1", "2":"v2", "3":"v3"}
    if char.char in charConvert and charConvert[char.char] in verses:
        currVerse = charConvert[char.char]
        currSlide = 0
        orderMode = False
        updateSlide()

def nextSlide(a):
    global currSlide, currVerse, currVerseNum, orderMode
    if currSlide < len(verses[currVerse])-1:
        currSlide += 1
        updateSlide()
    elif orderMode and currVerseNum < len(order)-1:
        currVerseNum += 1
        currVerse = order[currVerseNum]
        currSlide = 0
        updateSlide()
    else:
        mainText.delete('1.0', END)

def prevSlide(a):
    global currSlide, currVerse, currVerseNum, orderMode
    if currSlide > 0:
        currSlide -= 1
        updateSlide()
    elif orderMode and currVerseNum > 0:
        currVerseNum -= 1
        currVerse = order[currVerseNum]
        currSlide = len(verses[currVerse])-1
        updateSlide()
    else:
        mainText.delete('1.0', END)

def updateSlide():
    mainText.delete('1.0', END)
    mainText.insert(END, verses[currVerse][currSlide], 'main')

def restartSong(a):
    global currVerse, currVerseNum, currSlide, orderMode
    currVerseNum = 0
    currVerse = order[0]
    currSlide = 0
    orderMode = True
    updateSlide()

def nextSong(a):
    global currSong, songlist, song
    currSong += 1
    song = json.load(open(os.getcwd()+"/songs/"+songlist[currSong]+".json"))
    updateSong()

def updateSong():
    global song, verses, order, currVerseNum, currVerse, currSlide
    verses = {}
    for a in range(len(song["lyrics"])):
        verses[song["lyrics"][a]["id"]] = []
        for b in range(len(song["lyrics"][a]["slides"])):
            verses[song["lyrics"][a]["id"]].append(song["lyrics"][a]["slides"][b])
    for a in range(len(song["order"])):
        order.append(song["order"][a])
    currVerseNum = 0
    currVerse = order[currVerseNum]
    currSlide = 0
    updateSlide()

updateSong()
root.config(bg=theme['bgColour'])
mainText.tag_configure('main', justify='center', background=theme['bgColour'], foreground=theme['fgColour'], font=(theme['font'], theme['fontSize']), wrap='word')
mainText.bind("<Key>", setVerse)
mainText.bind("<Left>", prevSlide)
mainText.bind("<Right>", nextSlide)
mainText.bind("<Down>", nextSong)
mainText.bind("r", restartSong)
restartSong(0)
textFrame.pack(expand=True, fill='both', side=TOP)
mainText.pack(expand=True, fill='both')
logoBox.config(bg=theme['bgColour'])
logoBox.pack(expand=FALSE, fill=X, side=BOTTOM)
leftLogo.pack(side=LEFT, fill=Y, expand=FALSE)
rightLogo.pack(side=RIGHT, fill=Y, expand=FALSE)
root.mainloop()
