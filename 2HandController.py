import ctypes
import time
import cv2
import numpy as np
import HandTrackingModule3 as htm
import time
import autopy
import pyautogui
import pydirectinput


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



##########################
wCam, hCam = 640, 480
frameR = 100  # Frame Reduction
smoothening = 8
#########################

pTime = 0
plocX, plocY = 0, 0
clocX, clocY = 0, 0

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
detector = htm.handDetector()

wScr, hScr = autopy.screen.size()
print(wScr, hScr)


while True:

    success, img = cap.read()
    #img = cv2.flip(img, 1)
    img = detector.findHands(img)

    lmList,bbox = detector.findPosition(img)


    if len(lmList) != 0:
        fingers = detector.fingersUp()
        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                      (255, 0, 255), 2)


        if lmList[0][3] == 1:
            print("sol")


            if lmList[12][2] < lmList[10][2] and lmList[8][2] < lmList[6][2] and lmList[20][2] > lmList[18][2] and lmList[4][1] > lmList[3][1]:
                #up
                PressKey(0x11)
                #PressKey(0x26)
                #PressKey(0xC8)
                time.sleep(1)
                ReleaseKey(0x11)
                print("Up")
            if lmList[12][2] < lmList[10][2] and lmList[8][2] < lmList[6][2] and lmList[20][2] < lmList[18][2] and lmList[4][1] > lmList[3][1]:
                     #left and Up
                     PressKey(0x1E)
                     PressKey(0x11)
                     #PressKey(0x25)
                     #PressKey(0xCB)
                     # time.sleep(1)
                     ReleaseKey(0x1E)
                     ReleaseKey(0x11)
                     print("Left and Up")
            if lmList[12][2] < lmList[10][2] and lmList[8][2] < lmList[6][2] and lmList[20][2] > lmList[18][2] and lmList[4][1] < lmList[3][1]:
                #Right and Up
                     PressKey(0x20)
                     PressKey(0x11)
                     #PressKey(0x25)
                     #PressKey(0xCB)
                     # time.sleep(1)
                     ReleaseKey(0x20)
                     ReleaseKey(0x11)
                     print("Right and Up")
            if lmList[12][2] > lmList[10][2] and lmList[8][2] > lmList[6][2] and lmList[20][2] < lmList[18][2] and lmList[4][1] > lmList[3][1]:
                #left
                PressKey(0x1E)
                #PressKey(0x25)
                #PressKey(0xCB)
                time.sleep(1)
                ReleaseKey(0x1E)
                print("Left")
            if lmList[12][2] > lmList[10][2] and lmList[8][2] > lmList[6][2] and lmList[20][2] > lmList[18][2] and lmList[4][1] < lmList[3][1]:
                #Right
                PressKey(0x20)
                #PressKey(0x27)
                #PressKey(0xCD)
                time.sleep(1)
                ReleaseKey(0x20)
                print("Right")

            if lmList[12][2] > lmList[10][2] and lmList[8][2] > lmList[6][2] and lmList[20][2] > lmList[18][2] and lmList[4][1] > lmList[3][1]:
                #Down
                PressKey(0x1F)
                #PressKey(0x28)
                #PressKey(0xD0)
                time.sleep(1)
                ReleaseKey(0x1F)
                print("Down")

        if lmList[0][3] == 0:

            x1, y1 = lmList[8][1:3]
            x2, y2 = lmList[12][1:3]
            print("sag")

            if lmList[8][2] < lmList[6][2]:

                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                pydirectinput.moveTo(int(wScr - clocX), int(clocY))

                cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                plocX, plocY = clocX, clocY


            if lmList[8][2] < lmList[6][2] and lmList[12][2] < lmList[10][2]:

                lengthRC, img, lineInfoRC = detector.findDistance(8, 12, img)

                if lengthRC > 100:
                    cv2.circle(img, (lineInfoRC[4], lineInfoRC[5]),
                               15, (0, 255, 0), cv2.FILLED)
                    pyautogui.click(button='right')

                    print("Right Click")
            if lmList[8][2] < lmList[6][2] and lmList[4][1] > lmList[3][1]:
                lengthLC, img, lineInfoLC = detector.findDistance(4, 8, img)

                cv2.circle(img, (lineInfoLC[4], lineInfoLC[5]),
                           15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

                print("Left Click")


        try:
            if lmList[21][3] == 0:
                x1, y1 = lmList[29][1:3]
                x2, y2 = lmList[33][1:3]
                print("sag")
                print(fingers[5])
                if lmList[29][2] < lmList[27][2]:

                    x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                    y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

                    clocX = plocX + (x3 - plocX) / smoothening
                    clocY = plocY + (y3 - plocY) / smoothening


                    pydirectinput.moveTo(int(wScr - clocX), int(clocY))

                    cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
                    plocX, plocY = clocX, clocY


                if lmList[29][2] < lmList[27][2] and lmList[33][2] < lmList[31][2]:

                    lengthRC, img, lineInfoRC = detector.findDistance(8, 12, img)

                    if lengthRC > 100:
                        cv2.circle(img, (lineInfoRC[4], lineInfoRC[5]),
                                   15, (0, 255, 0), cv2.FILLED)
                        pyautogui.click(button='right')

                        print("Right Click")
                if lmList[29][2] < lmList[27][2] and lmList[25][1] < lmList[24][1]:
                    lengthLC, img, lineInfoLC = detector.findDistance(4, 8, img)

                    cv2.circle(img, (lineInfoLC[4], lineInfoLC[5]),
                               15, (0, 255, 0), cv2.FILLED)
                    autopy.mouse.click()

                    print("Left Click")

            else:
                print("sol")

                if lmList[33][2] < lmList[31][2] and lmList[29][2] < lmList[27][2] and lmList[41][2] > lmList[39][2] and lmList[25][1] > lmList[24][1]:
                    # up
                    PressKey(0x11)
                    # PressKey(0x26)
                    # PressKey(0xC8)
                    time.sleep(1)
                    ReleaseKey(0x11)
                    print("Up")
                if lmList[33][2] < lmList[31][2] and lmList[29][2] < lmList[27][2] and lmList[41][2] < lmList[39][2] and lmList[25][1] > lmList[24][1]:
                    # left and Up
                    PressKey(0x1E)
                    PressKey(0x11)
                    # PressKey(0x25)
                    # PressKey(0xCB)
                    # time.sleep(1)
                    ReleaseKey(0x1E)
                    ReleaseKey(0x11)
                    print("Left and Up")
                if lmList[33][2] < lmList[31][2] and lmList[29][2] < lmList[27][2] and lmList[41][2] > lmList[39][2] and lmList[25][1] < lmList[24][1]:
                    # Right and Up
                    PressKey(0x20)
                    PressKey(0x11)
                    # PressKey(0x25)
                    # PressKey(0xCB)
                    # time.sleep(1)
                    ReleaseKey(0x20)
                    ReleaseKey(0x11)
                    print("Right and Up")
                if lmList[33][2] > lmList[31][2] and lmList[29][2] > lmList[27][2] and lmList[41][2] < lmList[39][2] and lmList[25][1] > lmList[24][1]:
                    # left
                    PressKey(0x1E)
                    # PressKey(0x25)
                    # PressKey(0xCB)
                    time.sleep(1)
                    ReleaseKey(0x1E)
                    print("Left")
                if lmList[33][2] > lmList[31][2] and lmList[29][2] > lmList[27][2] and lmList[41][2] > lmList[39][2] and lmList[25][1] < lmList[24][1]:
                    # Right
                    PressKey(0x20)
                    # PressKey(0x27)
                    # PressKey(0xCD)
                    time.sleep(1)
                    ReleaseKey(0x20)
                    print("Right")


                if lmList[33][2] > lmList[31][2] and lmList[29][2] > lmList[27][2] and lmList[41][2] > lmList[39][2] and lmList[25][1] > lmList[24][1]:
                    # Down
                    PressKey(0x1F)
                    # PressKey(0x28)
                    # PressKey(0xD0)
                    time.sleep(1)
                    ReleaseKey(0x1F)
                    print("Down")
        except:
            pass


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    img = cv2.flip(img, 1)
    cv2.putText(img, str(int(fps)), (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    
    cv2.waitKey(1)

