#!/usr/bin/env python3
import os
import yaml

def getThemeList():
    global themes
    themes = os.listdir(os.getcwd()+"/themes/")

def fromConfig():
    global themeName
    with open(os.path.join(os.getcwd(),"config.yml"), 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    themeName = cfg['theme']
    setTheme()

def setTheme():
    global themeName
    with open(os.getcwd()+"/themes/"+themeName+".yml") as ymlfile1:
        theme = yaml.load(ymlfile1)
