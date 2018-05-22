#! /usr/bin/env python3
from xml.etree import ElementTree
import base64
from rmRTF import striprtf
import os
import json

path = os.getcwd()+"/testFiles"
song = ElementTree.parse(path+"/Be Enthroned.pro6")
tl = song.getroot()

songdata = {}
lookup = {"Verse 1":"v1","Verse 2":"v2", "Verse 3":"v3", "Verse 4":"v4", "Chorus 1":"c1", "(Bridge)":"b1", "(Ending)":"e1", "(Pre Chorus)":"p1"}
songname = tl.attrib['CCLISongTitle'] 
author = tl.attrib['CCLIAuthor']
songdata["title"] = songname
songdata["author"] = author
lyrics = []
order = []
currVerseNum = 0
for verse in tl.iter('RVSlideGrouping'):
    print(verse.attrib['name'])
    vname = verse.attrib['name']
    vref = lookup[vname]
    lyrics.append({"id":vref, "slides":[]})
    order.append(vref)
    for slide in verse.iter('NSString'):
        if slide.attrib['rvXMLIvarName'] == 'RTFData':
            slideText = striprtf(base64.standard_b64decode(slide.text))[:-1] 
            print(slideText)
            lyrics[currVerseNum]["slides"].append(slideText)
    currVerseNum += 1

songdata.update({"lyrics" : lyrics})
songdata["order"] = order
with open(os.getcwd()+"/songs/"+songname+".json", 'w') as outfile:
    json.dump(songdata, outfile, sort_keys=True, indent=4)
print(songdata)
