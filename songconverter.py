#!/usr/bin/env python3
from tkinter import *
import json
import os

title = ""
lyrics = []
author = ""
order = []
currVerse = ""
currVerseNum = -1
currSlide = 1
chars = {'c':1,'v':1,'b':1,'p':1,'e':1,'o':1}

root = Tk()

def moveSlide(char):
    global currVerse, currVerseNum, currSlide, chars
    nums = ['0','1','2','3','4','5','6','7','8','9']
    if char.char in chars:
        currVerse = char.char + str(chars[char.char])
        lyrics.append({"id":currVerse, "slides":[]})
        orderText.insert(END, currVerse + " ")
        chars[char.char] += 1
        currSlide = 0
        currVerseNum += 1
    elif char.char == "d":
        importText.delete(1.0,2.0)
    elif char.char in nums:
        if currVerse == "":
            currVerse = "v1"
            lyrics.append({"id":currVerse, "slides":[]})
            orderText.insert(END, currVerse + " ")
            chars["v"] += 1
            currSlide = 1
            currVerseNum += 1
        sendString = ""
        for i in range(0, int(char.char)):
            outputSongs.insert(END, currVerse + ":" + str(currSlide) + ": " + importText.get(1.0,"1.end"))
            sendString += (importText.get(1.0,"1.end") + "\n")
            importText.delete(1.0,2.0)
        lyrics[currVerseNum]["slides"].append(sendString)
    currSlide += 1

def saveSong():
    global lyrics, order, title, author
    print("saving...")
    jsonfile = {}
    jsonfile["title"] = titleText.get(1.0, "1.end")
    jsonfile["author"] = authorText.get(1.0, "1.end")
    jsonfile.update({"lyrics" : lyrics})
    jsonfile["order"] = orderText.get(1.0, "1.end").split()
    with open(os.getcwd()+"/songs/"+titleText.get(1.0, "1.end")+".json", 'w') as outfile:
        json.dump(jsonfile, outfile, sort_keys=True, indent=4)

topFrame = Frame(master=root)
topFrame.pack(fill=X, side=TOP)
topFrame1 = Frame(master=topFrame)
topFrame1.pack(fill=Y, side=LEFT)
topFrame2 = Frame(master=topFrame)
topFrame2.pack(fill=BOTH, expand=1, side=LEFT)
label1 = Label(topFrame1, text="Title:", justify=RIGHT)
label1.pack(side=TOP, pady=2)
titleText = Text(topFrame2, width=10, height=1)
titleText.pack(fill=X, side=TOP, padx=10, pady=2)
label2 = Label(topFrame1, text="Author:", justify=RIGHT)
label2.pack(side=TOP, pady=2)
authorText = Text(topFrame2, width=10, height=1)
authorText.pack(fill=X, side=TOP, padx=10, pady=2)
midFrame = Frame(master=root)
midFrame.pack(fill=BOTH, side=LEFT)
importText = Text(midFrame, width=35, height=20)
importText.pack(fill=Y, side=LEFT, padx=10, pady=2)
midFrame1 = Frame(master=midFrame)
midFrame1.pack(fill=BOTH, side=LEFT)
label3 = Label(midFrame1, text="Order:")
label3.pack(side=TOP)
orderText = Text(midFrame1, width=10, height=1)
orderText.pack(fill=X, side=TOP)
keyRegister = Text(midFrame1, width=20, height=5, bg='black')
keyRegister.pack(fill=X, expand=1, side=TOP)
outputSongs = Listbox(midFrame, width = 40)
outputSongs.pack(fill=Y,side=LEFT, padx=10, pady=2)
saveButton = Button(midFrame1, text="Save", command=saveSong)
saveButton.pack(side=TOP)

keyRegister.bind("<Key>", moveSlide)
root.mainloop()
