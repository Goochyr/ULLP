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
    niv = ElementTree.parse(path+"/NIV.xml")
    tl = niv.getroot()
    getReference()
    translateReference(instr)
    getPassage(book, chapter, verse1, verse2)
    print(passages[instr].verses)
else:
    import modules.screenControl as sC
    path = os.getcwd()+"/bibles"
    niv = ElementTree.parse(path+"/NIV.xml")
    tl = niv.getroot()
    currSlide = 0
    currPassage = ""
    blanked = False
    typing = False
    reference = ""
    currPassageNum = 0

def setSlide():
    global passages, currPassage, currSlide
    sC.updateText(passages[currPassage].verses[currSlide])

def nextSlide():
    global currSlide
    if currSlide < len(passages[currPassage].verses)-1:
        currSlide +=1
        setSlide()

def createPassage():
    global reference, book, chapter, verse1, verse2, currPassage, tl
    translateReference(reference)
    getPassage(book, chapter, verse1, verse2)
    currPassage = reference
   
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

def beginRef():
    global reference, typing
    reference = ""
    typing = True

def addRef(char):
    global reference
    reference += char

def rmRef():
    global reference
    reference = reference[:-1]
