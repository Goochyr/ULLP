#! /usr/bin/env python3
from xml.etree import ElementTree
import os

passages = {}
passageLookup = []

class Passage:
    def __init__(self, namein, versionin):
        self.name = namein
        self.version = versionin
        self.verses = []

    def addVerse(self,versein):
        self.verses.append(versein)


def getPassage(ibook, ichapter, v1, v2):
    global passages, reference
    passages[reference] = Passage(reference, 'niv')
    passageLookup.append(reference)
    for book in tl.findall('b'):
        if book.get('n').replace(" ","") == ibook:
            for chapter in book.findall('c'):
                if chapter.get('n') == ichapter:
                    for verse in chapter.findall('v'):
                        if int(verse.get('n')) >= int(v1) and int(verse.get('n')) <= int(v2):
                                #print(verse.get('n')+" "+verse.text)
                                passages[reference].addVerse(str(verse.get('n')+" "+verse.text))
                                #print(passages[instr].verses)

def translateReference(input):
    global book, chapter, verse1, verse2
    book = input.split(" ")[0]
    chapter = input.split(" ")[1].split(":")[0]
    verse1 = input.split(" ")[1].split(":")[1].split("-")[0]
    verse2 = input.split(" ")[1].split(":")[1].split("-")[1]

def getReference():
    global reference
    reference = input("Bible Reference: ")

if __name__ == "__main__":
    path = os.pardir+"/bibles"
    kjv = ElementTree.parse(path+"/KJV.xml")
    tl = kjv.getroot()
    getReference()
    translateReference(instr)
    getPassage(book, chapter, verse1, verse2)
    print(passages[instr].verses)
else:
    import modules.core.screenControl as sC
    path = os.getcwd()+"/bibles"
    kjv = ElementTree.parse(path+"/KJV.xml")
    tl = kjv.getroot()
    currSlide = 0
    currPassage = ""
    blanked = False
    typing = False
    reference = ""
    currPassageNum = 0
    bibles = []

def setSlide():
    global passages, currPassage, currSlide
    sC.updateText(passages[currPassage].verses[currSlide])

def nextSlide():
    global currSlide
    if currSlide < len(passages[currPassage].verses)-1:
        currSlide +=1
        setSlide()

def setTranslation(transCode):
    global tl
    bible = ElementTree.parse(path+"/"+transCode.upper()+".xml")
    tl = bible.getroot()

def createPassage():
    global reference, book, chapter, verse1, verse2, currPassage, currSlide, currPassageNum, passageLookup
    translateReference(reference)
    getPassage(book, chapter, verse1, verse2)
    currPassage = passageLookup[currPassageNum]
    currSlide = 0

def goLive():
    setSlide()

def prevSlide():
    global currSlide
    if currSlide > 0:
        currSlide -=1
        setSlide()

def restartPassage():
    global currSlide
    currSlide = 0
    setSlide()

def blankSlide():
    sC.blankText()

def nextPassage():
    global currPassage, currPassageNum, currSlide, passageLookup
    if currPassageNum < len(passageLookup)-1:
        currPassageNum += 1
        currPassage = passageLookup[currPassageNum]
        currSlide = 0
        setSlide()

def prevPassage():
    global currPassage, currPassageNum, currSlide, passageLookup
    if currPassageNum > 0:
        currPassageNum -= 1
        currPassage = passageLookup[currPassageNum]
        currSlide = 0
        setSlide()

def getAvailableBibles():
    global bibles
    bibles = os.listdir(os.getcwd()+"/bibles/")
    for a in range(len(bibles)):
        bibles[a] = bibles[a][:-4]
