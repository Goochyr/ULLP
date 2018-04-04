import modules.displaySong as dS
import modules.setlistHandler as sH
import modules.bibleHandler as bH
import modules.screenControl as sC

def bible(key):
    if bH.typing:
        print(key.keysym)
        if len(key.keysym) == 1 and key.keysym.isalpha():
            bH.addRef(key.keysym)
        elif len(key.keysym) == 1 and key.keysym.isdigit():
            bH.addRef(key.keysym)
        elif key.keysym == "colon":
            bH.addRef(":")
        elif key.keysym == "space":
            bH.addRef(" ")
        elif key.keysym == "minus":
            bH.addRef("-")
        elif key.keysym == "Return":
            bH.createPassage()
            bH.typing = False
        elif key.keysym == "BackSpace":
            bH.rmRef()
    else:
        if key.keysym == "Right" or key.keysym == "l":
            bH.nextSlide()
        elif key.keysym == "Left" or key.keysym == "h":
            bH.prevSlide()
        elif key.keysym == "t":
            sC.toggleBlanked()
        elif key.keysym =="r":
            bH.restartPassage()
        elif key.keysym =="Return":
            bH.goLive()
        elif key.keysym == "slash":
            bH.beginRef()

def live(key):
    if key.keysym == "Right" or key.keysym == "l":
        dS.nextSlide()
    elif key.keysym == "Left" or key.keysym == "h":
        dS.prevSlide()
    elif key.keysym =="r":
        dS.restartSong()
    elif key.keysym == "Up" or key.keysym == "k":
        dS.prevSong()
    elif key.keysym == "Down" or key.keysym == "j":
        dS.nextSong()
    elif key.keysym == "t":
        sC.toggleBlanked()
    elif key.keysym =="Return":
        sC.goLive()
    else:
        dS.setVerse(key)

def normal(key):
    if key.keysym == "l":
        return "live"
    elif key.keysym == "s":
        return "setlist"
    elif key.keysym == "b":
        return "bible"
    else:
        return

def setlist(key):
    if sH.searching:
        if len(key.keysym) == 1 and key.keysym.isalpha():
            sH.addSearch(key.keysym)
        elif key.keysym == "Space":
            sH.addSearch("Space")
        elif key.keysym == "Return":
            sH.endSearch()
        elif key.keysym == "BackSpace":
            sH.rmSearch()
    else:
        if key.keysym == "Right" or key.keysym == "l":
            sH.addSong()
        elif key.keysym == "Left" or key.keysym == "h":
            sH.removeSong()
        elif key.keysym =="o":
            sH.switchList()
        elif key.keysym == "Up" or key.keysym == "k":
            sH.prevItem()
        elif key.keysym == "Down" or key.keysym == "j":
            sH.nextItem()
        elif key.keysym == "slash":
            sH.beginSearch()
        elif key.keysym == "Return":
            sH.refreshLib() 
