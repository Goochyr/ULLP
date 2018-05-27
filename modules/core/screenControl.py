#!/usr/bin/env python3
import tkinter as tk
import os
import yaml
from PIL import ImageTk, Image, ImageFont, ImageDraw
from screeninfo import get_monitors
import fontconfig as fc
import numpy as np

def init():
    global root, textStore, blanked, monitors, width, height, topGap, pad, fullWindow
    monitors = get_monitors()
    root = tk.Toplevel()
    root.geometry(str(monitors[1].width)+"x"+str( monitors[1].height)+"+"+str(monitors[0].width)+"+"+"0")
    root.overrideredirect(1)
    height = monitors[1].height
    width = monitors[1].width
    fullWindow = tk.Label(root)
    #fullWindow.pack(fill=tk.BOTH)
    fullWindow.pack()
    textStore = ""
    blanked = False
    topGap = 30
    pad = 10

def getThemeData():
    global themeName, img_pil, baseImg, font, width, height, img_full, topGap
    with open(os.path.join(os.getcwd(),"config.yml"), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    themeName = cfg['theme']
    with open(os.getcwd()+"/themes/"+themeName+".yml") as ymlfile1:
        theme = yaml.load(ymlfile1)
    img = np.zeros((height,width,3),np.uint8)
    img_pil = Image.fromarray(img)
    fontfamily = theme['font']
    fonts = fc.query(family=fontfamily,lang='en')
    for i in range(1, len(fonts)):
        if fonts[i].fontformat == 'TrueType':
            fontpath = fonts[i].file
            break
    font = ImageFont.truetype(fontpath, theme['fontSize'])
    if theme['leftImg'] != 'none':
        leftImgPath = os.getcwd()+"/logos/"+theme['leftImg']+".png"
        leftImg0 = Image.open(leftImgPath) 
        [limageSizeWidth, limageSizeHeight] = leftImg0.size
        leftRatio = (height*0.25)/limageSizeHeight
        leftImg0 = leftImg0.resize((int(leftRatio*limageSizeWidth), int(leftRatio*limageSizeHeight)), Image.ANTIALIAS)
        img_pil.paste(leftImg0, (0,int(height*0.75)), leftImg0)
        img_full = img_pil.copy()

    if theme['rightImg'] != 'none':
        rightImgPath = os.getcwd()+"/logos/"+theme['rightImg']+".png"
        rightImg0 = Image.open(rightImgPath)
        w, h = rightImg0.size
        ratio = (height*0.75)/h
        rightImg0 = rightImg0.resize((int(ratio*w), int(ratio*h)), Image.ANTIALIAS)
        w, h = rightImg0.size
        img_full.paste(rightImg0, (int((width-w)/2),topGap))
        rightRatio = (height*0.25)/h
        rightImg0 = rightImg0.resize((int(rightRatio*w), int(rightRatio*h)), Image.ANTIALIAS)
        w, h = rightImg0.size
        img_pil.paste(rightImg0, (int(width-w),int(height*0.75)))
    baseImg = img_pil

def wrapText(text):
    global font, width, pad
    maxWidth = width-pad
    lines = []
    for line in text:
        if font.getsize(line)[0] <= maxWidth:
            lines.append(line)
        else:
            words = line.split(' ')
            i=0
            while i<len(words):
                newLine = ''
                while i<len(words) and font.getsize(newLine+words[i])[0] <= maxWidth:
                    newLine += words[i] + " "
                    i += 1
                if not newLine:
                    newLine = words[i]
                    i += 1
                lines.append(newLine)
    return lines


def updateText(text):
    global textStore, blanked, img_pil, baseImg, topGap, pad, font, fullWindow
    lines = []
    if not blanked:
        lines = text.split("\n")
        lines = wrapText(lines)
        img_pil = baseImg.copy()
        draw = ImageDraw.Draw(img_pil)
        cHeight = topGap
        for line in lines:
            w,h = font.getsize(line)
            draw.text(((width-w)/2,cHeight),line, font=font)
            cHeight += h+pad
        fullImg0 = ImageTk.PhotoImage(img_pil)
        fullWindow.config(image=fullImg0)
        fullWindow.image=fullImg0
    textStore = text
    #baseImg.show()

def blankText():
    global img_pil, baseImg, fullWindow
    img_pil = baseImg.copy()
    fullImg0 = ImageTk.PhotoImage(img_pil)
    fullWindow.config(image=fullImg0)
    fullWindow.image=fullImg0

def fullImg():
    global img_pil, img_full
    img_pil = img_full.copy()
    fullImg0 = ImageTk.PhotoImage(img_pil)
    fullWindow.config(image=fullImg0)
    fullWindow.image=fullImg0

def unFullImg():
    global blanked
    if blanked:
        blankText()
    else:
        unBlank()

def mainLoop():
    global root
    root.mainloop()

def unBlank():
    global textStore
    updateText(textStore)

def toggleBlanked():
    global blanked
    if blanked:
        blanked = False
        unBlank()
    else:
        blanked = True
        blankText()
