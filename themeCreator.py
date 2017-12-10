#!/usr/bin/env python3
from tkinter import *
import yaml
import os

allicons=os.listdir(os.getcwd()+"/logos/")
allicons.sort()
print(allicons)

root = Tk()

def useLeftImg():
    limgText.delete(1.0, END)
    limgText.insert(END, iconList.get(iconList.curselection()))

def useRightImg():
    rimgText.delete(1.0, END)
    rimgText.insert(END, iconList.get(iconList.curselection()))

def saveTheme():
    print("saving...")
    yamlFile = {}
    yamlFile['font'] = fontText.get(1.0, "1.end")
    yamlFile['fontSize'] = fsizeText.get(1.0, "1.end")
    yamlFile['bgColour'] = bgText.get(1.0, "1.end")
    yamlFile['fgColour'] = fgText.get(1.0, "1.end")
    yamlFile['leftImg'] = limgText.get(1.0, "1.end")
    yamlFile['rightImg'] = rimgText.get(1.0, "1.end")
    with open(os.getcwd()+"/themes/"+nameText.get(1.0, "1.end")+".yml", 'w') as outfile:
        yaml.dump(yamlFile, outfile, default_flow_style=False)


topFrame = Frame(master=root)
topFrame.pack(fill=X, side=TOP, padx=10, pady=2)
nameLabel = Label(topFrame, text="Name:", justify=RIGHT)
nameLabel.pack(side=LEFT)
nameText = Text(topFrame, width=10, height=1)
nameText.pack(fill=X, expand=True, side=LEFT)
midFrame = Frame(master=root)
midFrame.pack(fill=BOTH, expand=True, side=TOP, padx=10, pady=2)
midFrame1 = Frame(master=midFrame)
midFrame1.pack(fill=BOTH, side=LEFT)
bgLabel = Label(midFrame1, text="Background:", justify=RIGHT)
bgLabel.pack(side=TOP)
fgLabel = Label(midFrame1, text="Foreground:", justify=RIGHT)
fgLabel.pack(side=TOP)
iconList = Listbox(midFrame1)
iconList.pack(fill=BOTH, side=TOP, pady=5)
midFrame2 = Frame(master=midFrame)
midFrame2.pack(fill=BOTH, side=LEFT)
bgText = Text(midFrame2, width=30, height=1)
bgText.pack(fill=X, side=TOP)
fgText = Text(midFrame2, width=30, height=1)
fgText.pack(fill=X, side=TOP)
limgButton = Button(midFrame2, text="Use as left image", command=useLeftImg)
limgButton.pack(side=TOP, pady=5)
rimgButton = Button(midFrame2, text="Use as right image", command=useRightImg)
rimgButton.pack(side=TOP, pady=5)
saveButton = Button(midFrame2, text="Save", command=saveTheme)
saveButton.pack(side=TOP, pady=5)
midFrame3 = Frame(master=midFrame)
midFrame3.pack(fill=BOTH, side=LEFT)
fontLabel = Label(midFrame3, text="Font:", justify=RIGHT)
fontLabel.pack(side=TOP, fill=X)
fsizeLabel = Label(midFrame3, text="Font Size:", justify=RIGHT)
fsizeLabel.pack(side=TOP, fill=X)
limgLabel = Label(midFrame3, text="Left Image:", justify=RIGHT)
limgLabel.pack(side=TOP, fill=X)
rimgLabel = Label(midFrame3, text="Right Image:", justify=RIGHT)
rimgLabel.pack(side=TOP, fill=X)
midFrame4 = Frame(master=midFrame)
midFrame4.pack(fill=BOTH, side=LEFT)
fontText = Text(midFrame4, width=30, height=1)
fontText.pack(fill=X, side=TOP)
fsizeText = Text(midFrame4, width=30, height=1)
fsizeText.pack(fill=X, side=TOP)
limgText = Text(midFrame4, width=30, height=1)
limgText.pack(fill=X, side=TOP)
rimgText = Text(midFrame4, width=30, height=1)
rimgText.pack(fill=X, side=TOP)

for i in range(len(allicons)):
    iconList.insert(END, allicons[i][:-4])

root.mainloop()
