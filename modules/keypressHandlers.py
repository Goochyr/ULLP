import modules.displaySong as dS

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
        dS.toggleBlanked()
    else:
        dS.setVerse(key)

def normal(key):
    if key.keysym == "l":
        return "live"
    elif key.keysym == "s":
        return "setlist"
    else:
        return
