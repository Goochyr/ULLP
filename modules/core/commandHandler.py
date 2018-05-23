import modules.core.displaySong as dS
import modules.core.setlistHandler as sH
import modules.core.bibleHandler as bH
import modules.core.screenControl as sC

def doCommand(command):
    sendCommand=command.split()
    if sendCommand[0] == "bibleRef":
        if len(sendCommand) == 5:
            bibleRef(sendCommand[1]+sendCommand[2], sendCommand[3], sendCommand[4])
        elif len(sendCommand) == 4:
            bibleRef(sendCommand[1], sendCommand[2], sendCommand[3])
    elif sendCommand[0] == "getBibles":
        bH.getAvailableBibles()
    elif sendCommand[0] == "saveSetlist":
        sH.saveList(sendCommand[1])

def bibleRef(book, reference, translation):
    bH.reference = book+" "+reference
    bH.setTranslation(translation)
    bH.createPassage()
