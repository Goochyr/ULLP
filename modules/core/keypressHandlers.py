import modules.core.displaySong as dS
import modules.core.setlistHandler as sH
import modules.core.bibleHandler as bH
import modules.core.screenControl as sC

def bible(key):
    if key == "Right" or key == "l":
        bH.nextSlide()
    elif key == "Left" or key == "h":
        bH.prevSlide()
    elif key == "Down" or key == "j":
        bH.nextPassage()
    elif key == "Up" or key == "k":
        bH.prevPassage()
    elif key == "t":
        sC.toggleBlanked()
    elif key =="r":
        bH.restartPassage()
    elif key =="g":
        bH.goLive()

def live(key):
    if key == "Right" or key == "l":
        dS.nextSlide()
    elif key == "Left" or key == "h":
        dS.prevSlide()
    elif key =="r":
        dS.restartSong()
    elif key == "Up" or key == "k":
        dS.prevSong()
    elif key == "Down" or key == "j":
        dS.nextSong()
    elif key == "t":
        sC.toggleBlanked()
    elif key == "y":
        sC.fullImg()
    elif key == "u":
        sC.unFullImg()
    elif key =="g":
        dS.goLive()
    elif len(key) == 1:
        dS.setVerse(key)

def normal(key):
    if key == "l":
        return "live"
    elif key == "s":
        return "setlist"
    elif key == "b":
        return "bible"
    else:
        return

def setlist(key):
    if sH.searching:
        if len(key) == 1 and key.isalpha():
            sH.addSearch(key)
        elif key == "Space":
            sH.addSearch("Space")
        elif key == "Return":
            sH.endSearch()
        elif key == "BackSpace":
            sH.rmSearch()
    else:
        if key == "Right" or key == "l":
            sH.addSong()
        elif key == "Left" or key == "h":
            sH.removeSong()
        elif key =="o":
            sH.switchList()
        elif key == "Up" or key == "k":
            sH.prevItem()
        elif key == "Down" or key == "j":
            sH.nextItem()
        elif key == "slash":
            sH.beginSearch()
        elif key == "Return":
            sH.refreshLib() 
