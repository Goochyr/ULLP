#!/usr/bin/env python3
import tkinter as tk
import os
import yaml
from PIL import ImageTk, Image


def init():
    global root, rootWidth, rootHeight, mainText, textFrame, logoBox, leftLogo, rightLogo, theme, order, verses
    root = tk.Tk()
    rootHeight = root.winfo_screenheight()
    rootWidth = root.winfo_screenwidth()
    textFrame = tk.Frame(root, width=rootWidth, height=rootHeight*0.75, background='black')
    mainText = tk.Text(textFrame)
    logoBox = tk.Frame(root, width=rootWidth, height=rootHeight*0.25, background='black')
    logoBox.pack_propagate(0)
    leftLogo = tk.Label(logoBox, border=0, background='black')
    rightLogo = tk.Label(logoBox, border=0, background='black')
    textFrame.pack(expand=True, fill='both', side=tk.TOP)

def getThemeData():
    global mainText, leftLogo, rightLogo, themeName
    with open(os.path.join(os.getcwd(),"config.yml"), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    themeName = cfg['theme']
    with open(os.getcwd()+"/themes/"+themeName+".yml") as ymlfile1:
        theme = yaml.load(ymlfile1)
    mainText.config(background=theme['bgColour'], borderwidth=0, highlightthickness=0)
    mainText.tag_configure('main', justify='center', background=theme['bgColour'], foreground=theme['fgColour'], font=(theme['font'], theme['fontSize']), spacing1=30, wrap='word')
    if theme['leftImg'] != 'none':
        leftImgPath = os.getcwd()+"/logos/"+theme['leftImg']+".png"
        with Image.open(leftImgPath) as leftImg0:
            [limageSizeWidth, limageSizeHeight] = leftImg0.size
            leftRatio = (rootHeight*0.25)/limageSizeHeight
            leftImg0 = leftImg0.resize((int(leftRatio*limageSizeWidth), int(leftRatio*limageSizeHeight)), Image.ANTIALIAS)
            leftImg = ImageTk.PhotoImage(leftImg0)
            leftLogo.config(image=leftImg)
            leftLogo.image=leftImg
            leftImg0.close()

    if theme['rightImg'] != 'none':
        rightImgPath = os.getcwd()+"/logos/"+theme['rightImg']+".png"
        rightImg0 = Image.open(rightImgPath)
        [rimageSizeWidth, rimageSizeHeight] = rightImg0.size
        rightRatio = (rootHeight*0.25)/rimageSizeHeight
        rightImg0 = rightImg0.resize((int(rightRatio*rimageSizeWidth), int(rightRatio*rimageSizeHeight)), Image.ANTIALIAS)
        rightImg = ImageTk.PhotoImage(rightImg0)
        rightLogo.config(image=rightImg)
        rightLogo.image=rightImg
    mainText.pack(expand=True, fill='both', pady=20)
    logoBox.pack(expand=False, fill=tk.X, side=tk.BOTTOM)
    leftLogo.pack(side=tk.LEFT, fill=tk.Y, expand=False)
    rightLogo.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

def updateText(text):
    global mainText
    mainText.delete('1.0', tk.END)
    mainText.insert(tk.END, text, 'main')

def blankText():
    global mainText
    mainText.delete('1.0', tk.END)

def mainLoop():
    global root
    root.mainloop()

