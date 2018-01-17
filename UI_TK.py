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
currSlideNum = 0
order = []
orderMode = True
currSong = 0
blanked = False
live=True

UI = Tk()
root = Toplevel()
UI.winfo_toplevel().title("ULLP")
rootHeight = root.winfo_screenheight()
rootWidth = root.winfo_screenwidth()

def newSong():
    os.system("python3 songconverter.py")

textFrame = Frame(root, width=rootWidth, height=rootHeight*0.75, background='black')
mainText = Text(textFrame, background=theme['bgColour'], borderwidth=0, highlightthickness=0)
logoBox = Frame(root, width=rootWidth, height=rootHeight*0.25)
leftLogo = Label(logoBox, border=0, background='black')
rightLogo = Label(logoBox, border=0, background='black')

toolbar = Frame(UI, width=rootWidth, height=20)
toolbar.pack(side=TOP, fill=X, padx=5, pady=3)
newSongButton=Button(toolbar, text="New Song", command=newSong)
newSongButton.pack(side=LEFT)
versionLabel = Label(toolbar, text="Version: a0.0")
versionLabel.pack(side=LEFT)
mainFrame = Frame(UI, width=rootWidth, height=rootHeight-20)
mainFrame.pack(side=TOP, fill=BOTH, expand=True, padx=10, pady=10)
Label1 = Label(mainFrame, text="Library:")
Label1.grid(row=0, column=0)
Label2 = Label(mainFrame, text="Setlist:")
Label2.grid(row=0, column=1)
Label3 = Label(mainFrame, text="Slides:")
Label3.grid(row=0, column=2)
Label4 = Label(mainFrame, text="Details:")
Label4.grid(row=0, column=3)
libraryList = Listbox(mainFrame)
libraryList.grid(row=1, column=0, rowspan=3, sticky=N+E+S+W, padx=5)
setList = Listbox(mainFrame)
setList.grid(row=1, column=1, rowspan=3, sticky=N+E+S+W, padx=5)
slideList = Listbox(mainFrame)
slideList.grid(row=1, column=2, rowspan=3, sticky=N+E+S+W, padx=5)
detailFrame = Frame(mainFrame)
detailFrame.grid(row=1, column=3, sticky=N)
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
previewLabel.grid(row=2, column=3, sticky=S)
previewFrame = Frame(mainFrame, bg=theme['bgColour'], width=rootWidth*0.2, height=rootHeight*0.2)
previewFrame.grid(row=3, column=3)
previewFrame.pack_propagate(0)
previewTextFrame = Frame(previewFrame, bg=theme['bgColour'], width=rootWidth*0.1, height=rootHeight*0.15)
previewTextFrame.pack(side=TOP, fill=X, expand=False)
previewTextFrame.pack_propagate(0)
previewText = Text(previewTextFrame, background=theme['bgColour'], borderwidth=0, highlightthickness=0)
previewText.pack(side=TOP, expand=False, fill=X)
previewLogoBox = Frame(previewFrame, width=rootWidth*0.2, height=rootHeight*0.05, background=theme['bgColour'])
previewleftLogo = Label(previewLogoBox, border=0, background=theme['bgColour'])
previewrightLogo = Label(previewLogoBox, border=0, background=theme['bgColour'])
previewIndicator = Label(mainFrame, width=20, height=1, text='Live Mode', background='green')
previewIndicator.grid(row=4, column=3)
mainFrame.columnconfigure(0, weight=1)
mainFrame.columnconfigure(1, weight=1)
mainFrame.columnconfigure(2, weight=2)
mainFrame.columnconfigure(3, weight=1)
mainFrame.rowconfigure(1, weight=1)
mainFrame.rowconfigure(2, weight=1)

for i in range(len(allsongs)):
    libraryList.insert(END, allsongs[i][:-5])

for i in range(len(songlist)):
    setList.insert(END, songlist[i])

if theme['leftImg'] != 'none':
    leftImgPath = os.getcwd()+"/logos/"+theme['leftImg']+".png"
    with Image.open(leftImgPath) as leftImg0:
        [limageSizeWidth, limageSizeHeight] = leftImg0.size
        leftRatio = (rootHeight*0.25)/limageSizeHeight
        leftImg0 = leftImg0.resize((int(leftRatio*limageSizeWidth), int(leftRatio*limageSizeHeight)), Image.ANTIALIAS)
        leftImg = PIL.ImageTk.PhotoImage(leftImg0)
        leftLogo.config(image=leftImg)
        leftImg0 = leftImg0.resize((int(leftRatio*limageSizeWidth*0.2), int(leftRatio*limageSizeHeight*0.2)), Image.ANTIALIAS)
        leftImg1 = PIL.ImageTk.PhotoImage(leftImg0)
        previewleftLogo.config(image=leftImg1)
        leftImg0.close()

if theme['rightImg'] != 'none':
    rightImgPath = os.getcwd()+"/logos/"+theme['rightImg']+".png"
    rightImg0 = Image.open(rightImgPath)
    [rimageSizeWidth, rimageSizeHeight] = rightImg0.size
    rightRatio = (rootHeight*0.25)/rimageSizeHeight
    rightImg0 = rightImg0.resize((int(rightRatio*rimageSizeWidth), int(rightRatio*rimageSizeHeight)), Image.ANTIALIAS)
    rightImg = PIL.ImageTk.PhotoImage(rightImg0)
    rightLogo.config(image=rightImg)
    rightImg0 = rightImg0.resize((int(rightRatio*rimageSizeWidth*0.2), int(rightRatio*rimageSizeHeight*0.2)), Image.ANTIALIAS)
    rightImg1 = PIL.ImageTk.PhotoImage(rightImg0)
    previewrightLogo.config(image=rightImg1)

def setVerse(char):
    global currVerse, currSlide, orderMode, verses
    charConvert = {"c": "c1", "v":"v1", "b":"b1", "1":"v1", "2":"v2", "3":"v3"}
    if char.char in charConvert and charConvert[char.char] in verses:
        currVerse = charConvert[char.char]
        currSlide = 0
        orderMode = False
        updateSlide()
        highlightEntry()

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
        blankSlide(a)
    highlightEntry()

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
        blankSlide(a)
    highlightEntry()

def updateSlide():
    if blanked==False:
        mainText.delete('1.0', END)
        mainText.insert(END, verses[currVerse][currSlide], 'main')
        previewText.delete('1.0', END)
        previewText.insert(END, verses[currVerse][currSlide], 'main')
        currSongLabel1.config(text=songlist[currSong])
        currVerseLabel1.config(text=currVerse)
        currSlideLabel1.config(text=currSlide+1)

def blankSlide(a):
    global blanked
    if blanked:
        blanked=False
        updateSlide()
    else:
        mainText.delete('1.0', END)
        previewText.delete('1.0', END)
        blanked=True

def restartSong(a):
    global currVerse, currVerseNum, currSlide, orderMode
    currVerseNum = 0
    currVerse = order[0]
    currSlide = 0
    orderMode = True
    updateSlide()
    highlightEntry()

def nextSong(a):
    global currSong, songlist, song
    if currSong < len(songlist)-1:
        currSong += 1
        song = json.load(open(os.getcwd()+"/songs/"+songlist[currSong]+".json"))
        updateSong()
    else:
        blankSlide(a)

def prevSong(a):
    global currSong, songlist, song
    if currSong > 0:
        currSong -= 1
        song = json.load(open(os.getcwd()+"/songs/"+songlist[currSong]+".json"))
        updateSong()
    else:
        blankSlide(a)

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
    slideList.delete(0, END)
    for a in range(len(order)):
        for b in range(len(verses[order[a]])):
            slideList.insert(END, order[a]+" "+str(b+1)+" "+verses[order[a]][b])
    highlightEntry()
    updateSlide()

def highlightEntry():
    global currVerse, currSlide, order, orderMode, currVerseNum, songlist, currSong
    allSlides = slideList.get(0,END)
    if orderMode:
        numTimes = 0
        for a in range(0,currVerseNum+1):
            if order[a] == currVerse:
                numTimes += 1
        counter = 1
        for a in range(len(allSlides)):
            if allSlides[a][0:2] == currVerse and int(allSlides[a][3])-1 == currSlide:
                if counter == numTimes:
                    slideList.itemconfig(a, bg='green')
                    counter += 1
                else:
                    counter += 1
            else:
                slideList.itemconfig(a, bg='white')
    else:
        for a in range(len(allSlides)):
            if allSlides[a][0:2] == currVerse and int(allSlides[a][3])-1 == currSlide:
                slideList.itemconfig(a, bg='green')
            else:
                slideList.itemconfig(a, bg='white')
            
    for a in range(len(songlist)):
        if a == currSong:
            setList.itemconfig(a, bg='green')
        else:
            setList.itemconfig(a, bg='white')

def noliveMode(a):
    global live
    live=False
    previewIndicator.config(text="Normal Mode", background='red')

def liveMode(a):
    global live
    live=True
    previewIndicator.config(text="Live Mode", background='green')

updateSong()
root.config(bg=theme['bgColour'])
mainText.tag_configure('main', justify='center', background=theme['bgColour'], foreground=theme['fgColour'], font=(theme['font'], theme['fontSize']), spacing1=30, wrap='word')
previewText.tag_configure('main', justify='center', background=theme['bgColour'], foreground=theme['fgColour'], font=(theme['font'], int(theme['fontSize']*0.2)), wrap='word')
UI.bind("<Key>", setVerse)
UI.bind("<Left>", prevSlide)
UI.bind("<Right>", nextSlide)
UI.bind("<Down>", nextSong)
UI.bind("<Up>", prevSong)
UI.bind("r", restartSong)
UI.bind("t", blankSlide)
UI.bind("<Escape>", noliveMode)
UI.bind("l", liveMode)
restartSong(0)
textFrame.pack(expand=True, fill='both', side=TOP)
mainText.pack(expand=True, fill='both', pady=20)
logoBox.config(bg=theme['bgColour'])
logoBox.pack(expand=FALSE, fill=X, side=BOTTOM)
leftLogo.pack(side=LEFT, fill=Y, expand=FALSE)
rightLogo.pack(side=RIGHT, fill=Y, expand=FALSE)
previewLogoBox.pack(expand=False, fill=X, side=BOTTOM)
previewleftLogo.pack(side=LEFT, fill=Y)
previewrightLogo.pack(side=RIGHT, fill=Y)
root.mainloop()
UI.mainloop()
