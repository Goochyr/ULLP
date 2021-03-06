#!/usr/bin/env python3
import tkinter as tk
from tkinter import Frame, Text, Label, Listbox, Button, TOP, LEFT, RIGHT, BOTTOM, X, Y, BOTH, N, S, E, W, ttk
import modules.core.screenControl as sC
import modules.core.displaySong as dS
import modules.core.keypressHandlers as kH
import modules.core.setlistHandler as sH
import modules.core.bibleHandler as bH
import modules.core.commandHandler as cH
import os
from PIL import ImageTk, Image

mode = "live"
commandMode = False

version = open('version').read()[:-1]
UI = tk.Tk()
UI.winfo_toplevel().title("ULLP")
imgicon = ImageTk.PhotoImage(file=os.path.join(os.getcwd(),'icon.png'))
UI.tk.call('wm', 'iconphoto', UI._w, imgicon)
UI.tk_setPalette(background = "snow")
sC.init()
sC.getThemeData()
UI.geometry(str(sC.monitors[0].width)+'x'+str(sC.monitors[0].height)+'+0+0')

rootWidth = sC.monitors[0].width
rootHeight = sC.monitors[0].height

menubar = tk.Menu(UI)
importMenu = tk.Menu(menubar, tearoff=0)
importMenu.add_command(label="From ProPresenter")
importMenu.add_command(label="From SongPro")
menubar.add_cascade(label="Import", menu=importMenu)
setlistMenu = tk.Menu(menubar, tearoff = 0)
setlistMenu.add_command(label = "Open Setlist")
setlistMenu.add_command(label = "Save Setlist")
menubar.add_cascade(label="Setlist", menu=setlistMenu)
bibleMenu = tk.Menu(menubar, tearoff = 0)
bibleMenu.add_command(label = "Update Bibles")
bibleMenu.add_command(label = "Add Passage")
menubar.add_cascade(label="Bible", menu=bibleMenu)
themeMenu = tk.Menu(menubar, tearoff = 0)
themeMenu.add_command(label = "Get Themes")
themeMenu.add_command(label = "Set Theme")
menubar.add_cascade(label="Theme", menu=themeMenu)
menubar.add_command(label="Quit", command = UI.quit)
UI.config(menu=menubar)

toolbar = Frame(UI, width=rootWidth, height=20)
toolbar.pack(side=TOP, fill=X, padx=5, pady=3)
versionLabel = Label(toolbar, text="Version: "+version)
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
theme = tk.StringVar(UI)
theme.set(sC.themeName)
themeDropdown = ttk.Combobox(detailFrame)
themeDropdown['values']=(sC.themeName)
themeDropdown.current(0)
themeDropdown.grid(row=0, column=1)
#themeLabel1 = Label(detailFrame, text=sC.themeName)
#themeLabel1.grid(row=0, column=1)
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
bibleDropdown['values']=('KJV')
bibleDropdown.current(0)
bibleDropdown.grid(row=7, column=1)
previewLabel = Label(mainFrame, text="Preview:")
previewLabel.grid(row=2, column=3, sticky=S)
previewFrame = Label(mainFrame)
previewFrame.grid(row=3, column=3)
commandString = tk.StringVar()
searchBar = tk.Entry(mainFrame, textvariable=commandString)
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
        searchBar.delete(0, tk.END)
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
                searchBar.delete(0, tk.END)
                searchBar.insert(0,"bibleRef \"\" "+bibleDropdown.get())
                searchBar.icursor(10)
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
    if key.keysym == "slash" or key.keysym == "colon":
        searchBar.focus_set()
        commandMode = True
    elif key.keysym == "Return":
        commandMode = False
        mainFrame.focus_set()
        barText = commandString.get()
        commandString.set("")
        if barText.strip('\n').strip('\t') != "":
            barText = cH.doCommand(barText)
            commandString.set(barText)
            if mode == "bible":
                bibleUpdate()
                highlightBible()

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
    img_prev = sC.img_pil.copy()
    w, h = img_prev.size
    img_prev = img_prev.resize((int(w*0.2), int(h*0.2)), Image.ANTIALIAS)
    img_prev0 = ImageTk.PhotoImage(img_prev)
    previewFrame.config(image=img_prev0)
    previewFrame.image=img_prev0

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
    searchBar.delete(0, tk.END)
    if mode == "setlist": 
        searchBar.insert(0,sH.searchString)
    elif mode == "bible":
        searchBar.insert(0,bH.reference)

sH.init()
sH.fromConfig()
dS.init()
dS.updateSong()
dS.setSlide()
UI.bind("<Key>", keyPressSend)
sH.refreshLib()
updateInfo()
mainFrame.focus_set()
updateLists()
highlightSong()
cH.init()
cH.buildCommandTable()
sC.mainLoop()
UI.mainloop()
