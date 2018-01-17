import os

def init():
    global songlist, whichList, libSel, setSel
    songlist = []
    libSel = 0
    setSel = 0
    whichList = 0

def refreshLib():
    global allsongs
    allsongs=os.listdir(os.getcwd()+"/songs/")
    allsongs.sort()
