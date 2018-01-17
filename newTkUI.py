#!/usr/bin/env python3
import tkinter as tk
from tkinter import Frame, Label, Listbox, Button, TOP, LEFT, RIGHT, BOTTOM, X, Y, BOTH, N, S, E, W
import modules.screenControl as sC
import modules.displaySong as dS
import modules.keypressHandlers as kH
import os

mode = "live"

dS.init()
sC.init()
sC.getThemeData()
UI = tk.Toplevel()
UI.winfo_toplevel().title("ULLP")

toolbar = Frame(UI, width=sC.rootWidth, height=20)
toolbar.pack(side=TOP, fill=X, padx=5, pady=3)
versionLabel = Label(toolbar, text="Version: a0.0")
versionLabel.pack(side=LEFT)
mainFrame = Frame(UI, width=sC.rootWidth, height=sC.rootHeight-20)
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
themeLabel1 = Label(detailFrame, text=sC.themeName)
themeLabel1.grid(row=0, column=1)
setlistLabel = Label(detailFrame, text="Setlist:")
setlistLabel.grid(row=1, column=0)
setlistLabel1 = Label(detailFrame, text=dS.setlistName)
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
orderModeLabel = Label(detailFrame, text="Order Mode:")
orderModeLabel.grid(row=5, column=0)
orderModeLabel1 = Label(detailFrame)
orderModeLabel1.grid(row=5, column=1)
blankedLabel = Label(detailFrame, text="Blanked:")
blankedLabel.grid(row=6, column=0)
blankedLabel1 = Label(detailFrame)
blankedLabel1.grid(row=6, column=1)
previewLabel = Label(mainFrame, text="Preview:")
previewLabel.grid(row=2, column=3, sticky=S)
#previewFrame = Frame(mainFrame, bg=theme['bgColour'], width=rootWidth*0.2, height=rootHeight*0.2)
#previewFrame.grid(row=3, column=3)
#previewFrame.pack_propagate(0)
#previewTextFrame = Frame(previewFrame, bg=theme['bgColour'], width=rootWidth*0.1, height=rootHeight*0.15)
#previewTextFrame.pack(side=TOP, fill=X, expand=False)
#previewTextFrame.pack_propagate(0)
#previewText = Text(previewTextFrame, background=theme['bgColour'], borderwidth=0, highlightthickness=0)
#previewText.pack(side=TOP, expand=False, fill=X)
#previewLogoBox = Frame(previewFrame, width=rootWidth*0.2, height=rootHeight*0.05, background=theme['bgColour'])
#previewleftLogo = Label(previewLogoBox, border=0, background=theme['bgColour'])
#previewrightLogo = Label(previewLogoBox, border=0, background=theme['bgColour'])
previewIndicator = Label(mainFrame, width=20, height=1, text='Live Mode', background='green')
previewIndicator.grid(row=4, column=3)
mainFrame.columnconfigure(0, weight=1)
mainFrame.columnconfigure(1, weight=1)
mainFrame.columnconfigure(2, weight=2)
mainFrame.columnconfigure(3, weight=1)
mainFrame.rowconfigure(1, weight=1)
mainFrame.rowconfigure(2, weight=1)

allsongs=os.listdir(os.getcwd()+"/songs/")
allsongs.sort()

def keyPressSend(key):
    global mode
    if key.keysym == "Escape":
        mode = "normal"
    elif mode == "live":
        kH.live(key)
        updateLists()
    elif mode == "normal":
        a = kH.normal(key)
        if a in ["live", "setlist"]:
            mode = a
    updateInfo()
    highlightEntry()

def updateInfo():
    global mode
    currSongLabel1.config(text=dS.songlist[dS.currSong])
    currVerseLabel1.config(text=dS.currVerse)
    currSlideLabel1.config(text=dS.currSlide+1)
    orderModeLabel1.config(text=dS.orderMode)
    blankedLabel1.config(text=dS.blanked)
    if mode == "live":
        previewIndicator.config(text='Live Mode', background='green')
    elif mode == "normal":
        previewIndicator.config(text='Normal Mode', background='orange')
    elif mode == "setlist":
        previewIndicator.config(text='Setlist Mode', background='cyan')

def updateLists():
    global allsongs
    slideList.delete(0, tk.END)
    libraryList.delete(0, tk.END)
    setList.delete(0, tk.END)
    for i in range(len(allsongs)):
        libraryList.insert(tk.END, allsongs[i][:-5])
    for i in range(len(dS.songlist)):
        setList.insert(tk.END, dS.songlist[i])
    for a in range(len(dS.order)):
        for b in range(len(dS.verses[dS.order[a]])):
            slideList.insert(tk.END, dS.order[a]+" "+str(b+1)+" "+dS.verses[dS.order[a]][b])

def highlightEntry():
    allSlides = slideList.get(0,tk.END)
    if dS.orderMode:
        numTimes = 0
        for a in range(0,dS.currVerseNum+1):
            if dS.order[a] == dS.currVerse:
                numTimes += 1
        counter = 1
        for a in range(len(allSlides)):
            if allSlides[a][0:2] == dS.currVerse and int(allSlides[a][3])-1 == dS.currSlide:
                if counter == numTimes:
                    slideList.itemconfig(a, bg='green')
                    counter += 1
                else:
                    counter += 1
            else:
                slideList.itemconfig(a, bg='white')
    else:
        for a in range(len(allSlides)):
            if allSlides[a][0:2] == dS.currVerse:
                if int(allSlides[a][3])-1 == dS.currSlide:
                    slideList.itemconfig(a, bg='green')
                else:
                    slideList.itemconfig(a, bg='white')
            else:
                slideList.itemconfig(a, bg='gray70')
            
    for a in range(len(dS.songlist)):
        if a == dS.currSong:
            setList.itemconfig(a, bg='green')
        else:
            setList.itemconfig(a, bg='white')

dS.updateSong()
dS.setSlide()
UI.bind("<Key>", keyPressSend)
updateInfo()
updateLists()
sC.mainLoop()
UI.mainloop()
