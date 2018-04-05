#!/usr/bin/env python3
import tkinter as tk
from tkinter import Frame, Text, Label, Listbox, Button, TOP, LEFT, RIGHT, BOTTOM, X, Y, BOTH, N, S, E, W, ttk
import modules.screenControl as sC
import modules.displaySong as dS
import modules.keypressHandlers as kH
import modules.setlistHandler as sH
import modules.bibleHandler as bH
import modules.commandHandler as cH
import os

mode = "live"
commandMode = False

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
setlistLabel1 = Label(detailFrame)
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
bible = tk.StringVar(UI)
bible.set("KJV")
bibleLabel = Label(detailFrame, text="Bible:")
bibleLabel.grid(row=7, column=0)
bibleDropdown = ttk.Combobox(detailFrame)
bibleDropdown['values']=('NIV','KJV')
bibleDropdown.current(1)
bibleDropdown.grid(row=7, column=1)
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
searchBar = Text(mainFrame, height=1, width=30)
searchBar.grid(row=4, column=0, padx=5, columnspan=3, sticky=W+E)
previewIndicator = Label(mainFrame, width=20, height=1, text='Live Mode', background='green')
previewIndicator.grid(row=4, column=3)
mainFrame.columnconfigure(0, weight=1)
mainFrame.columnconfigure(1, weight=1)
mainFrame.columnconfigure(2, weight=2)
mainFrame.columnconfigure(3, weight=1)
mainFrame.rowconfigure(1, weight=1)
mainFrame.rowconfigure(2, weight=1)

def keyPressSend(key):
    global mode, commandMode
    if key.keysym == "Escape":
        mode = "normal"
        commandMode = False
        mainFrame.focus_set()
        resetHighlight()
        searchBar.delete("1.0", tk.END)
    if not commandMode:
        if mode == "live":
            kH.live(key.keysym)
            updateLists()
            highlightSong()
        elif mode == "bible":
            kH.bible(key.keysym)
            bibleUpdate()
            highlightBible()
            if key.keysym == "slash":
                searchBar.delete(1.0, tk.END)
                searchBar.insert(1.0,"bibleRef  "+bibleDropdown.get())
                searchBar.mark_set(tk.INSERT, '1.9')
                searchBar.focus_set()
        elif mode == "setlist":
            kH.setlist(key.keysym)
            setlistUpdate()
            searchbarUpdate()
        elif mode == "normal":
            a = kH.normal(key.keysym)
            if a == "live":
                mode = "live"
                updateLists()
                highlightSong()
            elif a == "setlist":
                mode = "setlist"
            elif a == "bible":
                mode = "bible"
                bibleUpdate()
                highlightBible()
                cH.doCommand('getBibles')
                bibleDropdown['values'] = bH.bibles
    if key.keysym == "slash":
        searchBar.focus_set()
        commandMode = True
    elif key.keysym == "Return":
        commandMode = False
        mainFrame.focus_set()
        barText = searchBar.get("1.0", tk.END)
        if barText.strip('\n').strip('\t') != "":
            cH.doCommand(barText)
            if mode == "bible":
                bibleUpdate()
                highlightBible()
        searchBar.delete("1.0", tk.END)

    updateInfo()

def updateInfo():
    global mode, commandMode
    setlistLabel1.config(text=sH.setlistName)
    if len(sH.songlist) > 0:
        currSongLabel1.config(text=sH.songlist[sH.currSong])
    else:
        currSongLabel1.config(text="Setlist Empty")
    currVerseLabel1.config(text=dS.currVerse)
    currSlideLabel1.config(text=dS.currSlide+1)
    orderModeLabel1.config(text=dS.orderMode)
    blankedLabel1.config(text=dS.blanked)
    if mode == "live":
        previewIndicator.config(text='Live Mode', background='green')
    elif mode == "bible":
        previewIndicator.config(text='Bible Mode', background='brown')
    elif mode == "normal":
        previewIndicator.config(text='Normal Mode', background='orange')
    elif mode == "setlist":
        setlistUpdate()
        previewIndicator.config(text='Setlist Mode', background='cyan')
    if commandMode:
        previewIndicator.config(text='Command Mode')

def updateLists():
    slideList.delete(0, tk.END)
    libraryList.delete(0, tk.END)
    setList.delete(0, tk.END)
    for i in range(len(sH.allsongs)):
        libraryList.insert(tk.END, sH.allsongs[i][:-5])
    for i in range(len(sH.songlist)):
        setList.insert(tk.END, sH.songlist[i])
    for a in range(len(dS.order)):
        for b in range(len(dS.verses[dS.order[a]])):
            slideList.insert(tk.END, dS.order[a]+" "+str(b+1)+" "+dS.verses[dS.order[a]][b])

def highlightSong():
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
            
    for a in range(len(sH.songlist)):
        if a == sH.currSong:
            setList.itemconfig(a, bg='green')
        else:
            setList.itemconfig(a, bg='white')

def highlightBible():
    allVerses = slideList.get(0, tk.END)
    allPassages = setList.get(0, tk.END)
    for a in range(len(allVerses)):
        if a == bH.currSlide:
            slideList.itemconfig(a, bg='brown')
        else:
            slideList.itemconfig(a, bg='white')
    for a in range(len(allPassages)):
        if allPassages[a] == bH.currPassage:
            setList.itemconfig(a, bg='brown')
        else:
            setList.itemconfig(a, bg='white')

def setlistUpdate():
    updateLists()
    if sH.whichList:
        for a in range(len(sH.songlist)):
            if a == sH.setSel:
                setList.itemconfig(a, bg='cyan')
            else:
                setList.itemconfig(a, bg='white')

    else:
        for a in range(len(sH.allsongs)):
            if a == sH.libSel:
                libraryList.itemconfig(a, bg='cyan')
            else:
                libraryList.itemconfig(a, bg='white')

def bibleUpdate():
    slideList.delete(0, tk.END)
    setList.delete(0, tk.END)
    for a in bH.passages:
        setList.insert(tk.END, a)
    if bH.currPassage != "":
        for a in bH.passages[bH.currPassage].verses:
            slideList.insert(tk.END, a)

def resetHighlight():
    for a in range(slideList.size()):
        slideList.itemconfig(a, bg='white')
    for a in range(setList.size()):
        setList.itemconfig(a, bg='white')
    for a in range(libraryList.size()):
        libraryList.itemconfig(a, bg='white')

def searchbarUpdate():
    global mode
    searchBar.delete('1.0', tk.END)
    if mode == "setlist": 
        searchBar.insert('1.0',sH.searchString)
    elif mode == "bible":
        searchBar.insert('1.0',bH.reference)

sH.init()
sH.fromConfig()
dS.init()
dS.updateSong()
dS.setSlide()
UI.bind("<Key>", keyPressSend)
sH.refreshLib()
updateInfo()
updateLists()
highlightSong()
sC.mainLoop()
UI.mainloop()
