import ctypes
import time
import cv2
import numpy as np
import HandTrackingModule as htm
import time


SendInput = ctypes.windll.user32.SendInput


W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
UP = 0xC8
LEFT = 0xCB
RIGHT = 0xCD
DOWN = 0xD0
ENTER = 0x1C
ESC = 0x01
TWO = 0x03

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
                        ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))




wCam, hCam = 640, 480


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector(maxHands=2)



while True:

    success, img = cap.read()
    img = detector.findHands(img)

    lmList, bbox = detector.findPosition(img)


    if len(lmList) != 0:
       # print(lmList)

        fingers = detector.fingersUp()

        if fingers[2] == 1 and fingers[0]==0 and fingers[4]== 0 and fingers[1]==1:
            #up
            #PressKey(0x11)
            #PressKey(0x26)
            PressKey(0xC8)
            time.sleep(0.5)
            ReleaseKey(0x11)


            print("Up")


        if fingers [2] == 0 and fingers[0] ==1:
            #left
            #PressKey(0x1E)
            #PressKey(0x25)
            PressKey(0xCB)
            time.sleep(0.5)
            ReleaseKey(0x1E)

            print("Left")
        if fingers[2] == 0 and fingers[4] == 1:
            #Right
            #PressKey(0x20)
            #PressKey(0x27)
            PressKey(0xCD)
            time.sleep(0.5)
            ReleaseKey(0x20)


            print("Right")
        if lmList[12][2] > lmList[10][2] and lmList[8][2] > lmList[6][2] and lmList[20][2] > lmList[18][2] and lmList[4][1] < lmList[3][1]:
            #print(lmList[8])
            #Down
            #PressKey(0x1F)
            #PressKey(0x28)
            PressKey(0xD0)
            time.sleep(0.5)
            ReleaseKey(0x1F)



            print("Down")

    img = cv2.flip(img, 1)
    cv2.imshow("Image", img)

    cv2.waitKey(1)

