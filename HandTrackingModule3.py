import cv2
import mediapipe as mp
import time
import math
import numpy as np


class handDetector():
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.7, trackCon = 0.7):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands  # Formalite olarak burda elleri tanimlamak gerekiyor
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)  # Standart degerleri kullaniyoruz sürekli algilama, 2 el vb.
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20, 25, 29, 33, 37, 41]#parmak uçları

    def get_label(self, index, hand, results):
        output = None
        for idx, classification in enumerate(self.results.multi_handedness):
            if classification.classification[0].index == index:
                # Process results
                label = classification.classification[0].label
                score = classification.classification[0].score
                text = '{} {}'.format(label, round(score, 2))

                # Extract Coordinates
                coords = tuple(np.multiply(
                    np.array((hand.landmark[self.mpHands.HandLandmark.WRIST].x,
                              hand.landmark[self.mpHands.HandLandmark.WRIST].y)),
                    [640, 480]).astype(int))

                output = text, coords

        return output

    def findHands(self, img, draw = True ):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) #hands sınıfı sadece rgb görüntü o yüzden renk değiştiridk
        self.results = self.hands.process(imgRGB)
        #print(results.multi_hand_landmarks)#Kamerada el olup olmadığını koordinatlarını öğrenme

        # if self.results.multi_hand_landmarks:
        #     for handLms in self.results.multi_hand_landmarks:# elleri sırayla çirdirmek için
        #         if draw:
        #             self.mpDraw.draw_landmarks(img, handLms,
        #                                        self.mpHands.HAND_CONNECTIONS)#el çizmek için(kamera,eldeki noktalar,noktaları birleştirme)
        # return img
        if self.results.multi_hand_landmarks:
            for num, hand in enumerate(self.results.multi_hand_landmarks):
                self.mpDraw.draw_landmarks(img, hand, self.mpHands.HAND_CONNECTIONS,
                                          self.mpDraw.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                                          self.mpDraw.DrawingSpec(color=(250, 44, 250), thickness=2, circle_radius=2),
                                          )



                # if self.get_label(num, hand, self.results):
                #     text, coord = self.get_label(num, hand, self.results)
                #     cv2.putText(img, text, coord, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        return img
 

    def findPosition(self, img, handNo=0, draw=True):
        xList = []
        yList = []
        bbox = []
        self.lmList = []
        self.lmList2 = []
        if self.results.multi_hand_landmarks:
            for i in range(len(self.results.multi_hand_landmarks)):
                myHand = self.results.multi_hand_landmarks[i]

                for id, lm in enumerate(myHand.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    xList.append(cx)
                    yList.append(cy)
                    # print(id, cx, cy)
                    self.lmList.append([id, cx, cy])

                    xmin, xmax = min(xList), max(xList)
                    ymin, ymax = min(yList), max(yList)
                    bbox = xmin, ymin, xmax, ymax

                    # if draw:
                    #     cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)





            sayac = 0

            for i in range(len(self.results.multi_hand_landmarks)):
                myHand = self.results.multi_hand_landmarks[i]

                for id, lm in enumerate(myHand.landmark):


                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if sayac <= 20:
                        if self.lmList[4][1] < self.lmList[20][1]:
                            el = 1
                            self.lmList2.append([id, cx, cy, el])
                            #print("sayac 20 sag")
                        elif self.lmList[4][1] > self.lmList[20][1]:
                            el = 0
                            self.lmList2.append([id, cx, cy, el])
                            #print("sayac 20 sol")

                    elif 20 < sayac < 42:
                        if self.lmList[25][1] < self.lmList[41][1]:
                            el = 1
                            self.lmList2.append([id, cx, cy, el])
                            #print("sayac 55 sag")
                        elif self.lmList[25][1] > self.lmList[41][1]:
                            el = 0
                            self.lmList2.append([id, cx, cy, el])
                            #print("sayac 55 sol")
                    sayac += 1
            if self.lmList2[0][3] == 1:
                pass
                #cv2.putText(img, "SAG", (self.lmList2[0][1],self.lmList2[0][2]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            else:
                pass
                #cv2.putText(img, "SOL", (self.lmList2[0][1], self.lmList2[0][2]), cv2.FONT_HERSHEY_SIMPLEX, 1,
                #            (255, 255, 255), 2, cv2.LINE_AA)
            try:
                if self.lmList2[21][3] == 1:
                    pass
                    #cv2.putText(img, "SOL", (self.lmList2[21][1],self.lmList2[21][2]), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                else:
                    pass
                    #cv2.putText(img, "SOL", (self.lmList2[21][1], self.lmList2[21][2]), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    #            (255, 255, 255), 2, cv2.LINE_AA)
            except:
                pass





        return self.lmList2,bbox

    def fingersUp(self):
        fingers = []
        # Thumb
        if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Fingers
        for id in range(1, 5):
            if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

            # totalFingers = fingers.count(1)
            # print(totalFingers)

        return fingers

    def findDistance(self, p1, p2, img, draw=True, r=15, t=3):
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
            cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        return length, img, [x1, y1, x2, y2, cx, cy]





def main():
    pTime = 0  # geçmiş zaman
    cTime = 0  # şimdiki zaman
    cap = cv2.VideoCapture(0)
    detector = handDetector()


    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img)
        lmList,img = detector.findPosition(img)

        if len(lmList) != 0:
            pass



        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        #cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                    #(255, 0, 255), 3)

        #cv2.imshow("image", img)
        cv2.waitKey(1)



if __name__ == "__main__":
    main()