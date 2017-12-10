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

allsongs=os.listdir(os.getcwd()+"/songs/")
allsongs.sort()

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
UI = Tk()

textFrame = Frame(root, width=rootWidth, height=rootHeight*0.75, background='black')
mainText = Text(textFrame, background=theme['bgColour'], borderwidth=0, foreground='black', highlightthickness=0)
logoBox = Frame(root, width=rootWidth, height=rootHeight*0.25)
leftLogo = Label(logoBox, border=0, background='black')
rightLogo = Label(logoBox, border=0, background='black')

toolbar = Frame(UI, width=rootWidth, height=20)
toolbar.pack(side=TOP, fill=X)
versionLabel = Label(toolbar, text="Version: a0.0")
versionLabel.pack(side=LEFT)
mainFrame = Frame(UI, width=rootWidth, height=rootHeight-20)
mainFrame.pack(side=TOP, fill=BOTH, expand=True)
Label1 = Label(mainFrame, text="Library:")
Label1.grid(row=0, column=0)
Label2 = Label(mainFrame, text="Setlist:")
Label2.grid(row=0, column=1)
Label3 = Label(mainFrame, text="Slides:")
Label3.grid(row=0, column=2)
Label4 = Label(mainFrame, text="Details:")
Label4.grid(row=0, column=3)
libraryList = Listbox(mainFrame)
libraryList.grid(row=1, column=0, rowspan=3, sticky=N+S)
setList = Listbox(mainFrame)
setList.grid(row=1, column=1, rowspan=3, sticky=N+S)
slideList = Listbox(mainFrame)
slideList.grid(row=1, column=2, rowspan=3, sticky=N+S)
detailFrame = Frame(mainFrame)
detailFrame.grid(row=1, column=3)
themeLabel = Label(detailFrame, text="Theme:")
themeLabel.grid(row=0, column=0)
themeLabel1 = Label(detailFrame, text=themeName)
themeLabel1.grid(row=0, column=1)
setlistLabel = Label(detailFrame, text="Setlist:")
setlistLabel.grid(row=1, column=0)
setlistLabel1 = Label(detailFrame, text=setlistName)
setlistLabel1.grid(row=1, column=1)
currSongLabel = Label(detailFrame, text="Current Song:")
currSongLabel.grid(row=2, column=0)
currSongLabel1 = Label(detailFrame)
currSongLabel1.grid(row=2, column=1)
currVerseLabel = Label(detailFrame, text="Current Verse:")
currVerseLabel.grid(row=3, column=0)
currVerseLabel1 = Label(detailFrame)
currVerseLabel1.grid(row=3, column=1)
currSlideLabel = Label(detailFrame, text="Current Slide:")
currSlideLabel.grid(row=4, column=0)
currSlideLabel1 = Label(detailFrame)
currSlideLabel1.grid(row=4, column=1)
previewLabel = Label(mainFrame, text="Preview:")
previewLabel.grid(row=2, column=3)
previewFrame = Frame(mainFrame, bg='black', width=rootWidth*0.2, height=rootHeight*0.2)
previewFrame.grid(row=3, column=3)
previewText = Text(previewFrame, background='green')
previewText.pack(fill=BOTH, side=TOP)
previewLogoBox = Frame(previewFrame)
previewLogoBox.pack(side=TOP)
previewleftLogo = Label(previewLogoBox, border=0, background='black')
previewleftLogo.pack(side=LEFT)
previewrightLogo = Label(previewLogoBox, border=0, background='black')
previewrightLogo.pack(side=LEFT)

for i in range(len(allsongs)):
    libraryList.insert(END, allsongs[i][:-5])

for i in range(len(songlist)):
    setList.insert(END, songlist[i])

if theme['leftImg'] != 'none':
    leftImgPath = os.getcwd()+"/logos/"+theme['leftImg']+".png"
    leftImg0 = Image.open(leftImgPath)
    [limageSizeWidth, limageSizeHeight] = leftImg0.size
    leftRatio = (rootHeight*0.25)/limageSizeHeight
    leftImg0 = leftImg0.resize((int(leftRatio*limageSizeWidth), int(leftRatio*limageSizeHeight)), Image.ANTIALIAS)
    leftImg = PIL.ImageTk.PhotoImage(leftImg0)
    leftLogo.config(image=leftImg)

if theme['rightImg'] != 'none':
    rightImgPath = os.getcwd()+"/logos/"+theme['rightImg']+".png"
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
    currSongLabel1.config(text=songlist[currSong])
    currVerseLabel1.config(text=currVerse)
    currSlideLabel1.config(text=currSlide)

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
previewText.bind("<Key>", setVerse)
previewText.bind("<Left>", prevSlide)
previewText.bind("<Right>", nextSlide)
previewText.bind("<Down>", nextSong)
previewText.bind("r", restartSong)
restartSong(0)
textFrame.pack(expand=True, fill='both', side=TOP)
mainText.pack(expand=True, fill='both')
logoBox.config(bg=theme['bgColour'])
logoBox.pack(expand=FALSE, fill=X, side=BOTTOM)
leftLogo.pack(side=LEFT, fill=Y, expand=FALSE)
rightLogo.pack(side=RIGHT, fill=Y, expand=FALSE)
root.mainloop()
UI.mainloop()
