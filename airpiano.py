import cv2 as cv
import numpy as np
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math


# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
# Get current volume
currentVolumeDb = volume.GetMasterVolumeLevel()
print (currentVolumeDb)


def Press(key):
    pyautogui.press(key)


cap = cv.VideoCapture(0)


# cap.set(3,600)
# cap.set(4,800)

def nothing(x):
    pass

while True:
    _, frame = cap.read()
    frame = cv.resize(frame, (1024, 768))
    frame = cv.flip(frame, 1)
    frame = cv.GaussianBlur(frame, (5, 5), 0)
    # frame=cv.cvtColor(frame,cv.COLOR_BGR2RGB)

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    lower_blue = np.array([100, 150, 80])  # get the proper values from experimenting with trackbar.
    upper_blue = np.array([130, 255, 255])
    lower_red = np.array([5, 150, 150])  # get the proper values from experimenting with trackbar.
    upper_red = np.array([10, 255, 255])


    mask = cv.inRange(hsv, lower_blue, upper_blue)
    maskVolume = cv.inRange(hsv, lower_red, upper_red)



    notes = ['C','D','E','F','G','A','B','C','D','E','F','G','A','B','C','D','E','F','G','A','B']
    keystroke =  ['t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n']

    firstx = 0
    notesCounter = 0
    for keysCounter in range (21):
        cv.rectangle(frame, (firstx, 400), (firstx+45, 768), (255, 255, 255), -1)
        cv.putText(frame, notes[notesCounter], (firstx+15, 720), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv.LINE_AA)

        firstx = firstx+50
        notesCounter = notesCounter+1

    cv.putText(frame, str(int(currentVolumeDb)+60), (20, 20), cv.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv.LINE_AA)

    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for contour in contours:
        if cv.contourArea(contour) > 400:
            M = cv.moments(contour)
            cx = int(M['m10'] / M['m00'])  # finding the center using Moments
            cy = int(M['m01'] / M['m00'])
            firstx = 0
            notesCounter = 0

            for keysCounter in range(21):
                if (cx > firstx and cx < firstx+45):
                    Press(keystroke[notesCounter])
                    cv.rectangle(frame, (firstx, 400), (firstx + 45, 768), (0, 0, 0), -1)
                firstx = firstx + 50
                notesCounter = notesCounter + 1



    contoursVolume, _ = cv.findContours(maskVolume, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    for contour in contoursVolume:
        if cv.contourArea(contour) > 200:
            M = cv.moments(contour)
            cx = int(M['m10'] / M['m00'])  # finding the center using Moments
            cy = int(M['m01'] / M['m00'])

            tempVolume = (1-((768 - cy)/768))*(-60)
            if (tempVolume > currentVolumeDb+10 or tempVolume < currentVolumeDb+10) :
                currentVolumeDb = tempVolume
                volume.SetMasterVolumeLevel(currentVolumeDb, None)


    cv.imshow('frame', frame)
    # cv.imshow('mask',mask)

    key = cv.waitKey(1)
    if key == 27:
        break;

cap.release()
cv.destroyAllWindows()