import cv2 as cv
import numpy as np
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
import time


def Press(key):
    pyautogui.press(key)


notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'A', 'B']
keystroke = ['t', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'z', 'x', 'c', 'v', 'b', 'n']

broederJacob = [7,8,9,7,7,8,9,7,9,10,11,99,9,10,11,99,11,12,11,10,9,7]
song = broederJacob

aantal = len(broederJacob)

print ("click piano screen")
time.sleep(2)

noot = 0
while noot in range(aantal):
    if (song[noot] == 99):
        time.sleep(0.25)
    else :
        Press(keystroke[song[noot]])
    time.sleep(0.5)
    noot+=1


