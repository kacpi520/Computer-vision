import mediapipe as mp
import cv2
import time
import pyautogui


class handDetector():
    def __init__(self, mode=False, maxHands=2, modelComp=1, complexity = 1, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.modelComp = modelComp
        self.complexity = complexity

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.complexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if len(lmList) >= 9:
                    # Indeks kciuka (4) i wskazującego palca (8)
                    thumb_x, thumb_y = lmList[4][1], lmList[4][2]
                    index_x, index_y = lmList[8][1], lmList[8][2]
                    cv2.line(img, (thumb_x, thumb_y), (index_x, index_y), (0, 255, 0), 5)
                    cv2.circle(img, (thumb_x, thumb_y), 15, (255, 0, 255), cv2.FILLED)
                    cv2.circle(img, (index_x, index_y), 15, (255, 0, 255), cv2.FILLED)
                    dist = ((thumb_x - index_x)**2 + (thumb_y - index_y)**2)**0.5
                    cv2.putText(img, "Odleglosc: " + str(int(dist)), (10, 90), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)
        return lmList


def main():
    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img)
        if len(lmList) != 0:
            print(lmList[8])

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(img, "FPS: " + str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 255), 3)


        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('q'): #kliknij q żeby wyjść
            break
if __name__ == "__main__":
    main()