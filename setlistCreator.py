#!/usr/bin/env python3
from tkinter import *
import json
import os

allsongs=os.listdir(os.getcwd()+"/songs/")
allsongs.sort()
songs=[]

root = Tk()

print(os.listdir(os.getcwd()+"/songs/"))

def addSong():
    setlist.insert(END, songlist.get(songlist.curselection()))

def saveSetlist():
    print("saving...")
    jsonfile={}
    songs = []
    for i in range(setlist.size()):
        songs.append(setlist.get(i))
    jsonfile["songs"]=songs
    with open(os.getcwd()+"/setlists/"+nameText.get(1.0, "1.end")+".json", 'w') as outfile:
        json.dump(jsonfile, outfile, sort_keys=True, indent=4)
    print(songs)

topFrame = Frame(master=root)
topFrame.pack(fill=X, side=TOP, padx=10, pady=2)
label1 = Label(topFrame, text="Name:", justify=RIGHT)
label1.pack(side=LEFT, pady=2)
nameText = Text(topFrame, width=10, height=1)
nameText.pack(fill=X, expand=True, side=LEFT)
midFrame = Frame(master=root)
midFrame.pack(fill=BOTH, expand=True, side=TOP, padx=10, pady=2)
songlist = Listbox(midFrame)
songlist.pack(fill=BOTH, expand=True, side=LEFT)
setlist = Listbox(midFrame)
setlist.pack(fill=BOTH, expand=True, side=LEFT)
bottomFrame = Frame(master=root)
bottomFrame.pack(fill=X, side=TOP, padx=10, pady=2)
addbutton = Button(bottomFrame, text="Add", command=addSong)
addbutton.pack(side=LEFT, pady=10)
savebutton = Button(bottomFrame, text="Save", command=saveSetlist)
savebutton.pack(side=RIGHT, pady=10)

for i in range(len(allsongs)):
    songlist.insert(END, allsongs[i][:-5])

root.mainloop()
