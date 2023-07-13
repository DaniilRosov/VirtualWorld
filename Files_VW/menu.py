import pygame
import sys
from settings import *
from background import Background
import ui
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import random
import numpy as np
import HandTrackingModule as htm
import os
from deepface import DeepFace

def rock():
    pygame.mixer.music.load("Assets/Sounds/music.wav")
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1)
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=1)

    timer = 0
    stateResult = False
    startGame = False
    error = False
    scores = [0, 0]  # ai,player
    result = ''
    while True:
        success, img = cap.read()

        hands = detector.findHands(img, draw=False)
        if startGame:
            if stateResult is False:
                playerMove = None
                timer = time.time() - initialTime

                (widthTxt1, heightTxt1), baseline = cv2.getTextSize("1", cv2.FONT_HERSHEY_PLAIN, 6, 4)
                heightWin = img.shape[0]
                widthWin = img.shape[1]
                x = (widthWin - widthTxt1) // 2
                y = (heightWin - heightTxt1) // 2 + 50
                cv2.putText(img, str(int(timer) + 1), (x, y), cv2.FONT_HERSHEY_PLAIN, 6, (231, 255, 252), 4)

                if timer > 2:
                    stateResult = True
                    timer = 0

                    if hands:
                        hand = hands[0]
                        fingers = detector.fingersUp(hand)
                        if fingers == [0, 0, 0, 0, 0]:
                            playerMove = 1
                        elif fingers == [1, 1, 1, 1, 1]:
                            playerMove = 2
                        elif fingers == [0, 1, 1, 0, 0]:
                            playerMove = 3
                        else:
                            result = "gest undefined"
                            error = True
                        if not error:
                            robotMove = random.randint(1, 3)
                            if playerMove == robotMove:
                                result = "Draw"
                            elif (playerMove == 1 and robotMove == 3) or \
                                    (playerMove == 2 and robotMove == 1) or \
                                    (playerMove == 3 and robotMove == 2):
                                result = "YOU WIN"
                                scores[1] += 1
                            elif (playerMove == 3 and robotMove == 1) or \
                                    (playerMove == 1 and robotMove == 2) or \
                                    (playerMove == 2 and robotMove == 3):
                                result = "YOU LOSE"
                                scores[0] += 1
                            imgAI = cv2.imread(f'Resources/rockpaper/{robotMove}.png', cv2.IMREAD_UNCHANGED)
                            img = cvzone.overlayPNG(img, imgAI, [400, 200])
                            print(fingers)
                            print(playerMove)
                    else:
                        result = 'hand  undefined'
                        error = True
            if stateResult and not error:
                img = cvzone.overlayPNG(img, imgAI, [400, 200])
            cv2.putText(img, f'Robot points: {scores[0]}', (350, 50), cv2.FONT_HERSHEY_PLAIN, 2, (103, 52, 43), 4)
            cv2.putText(img, f'Human points: {scores[1]}', (30, 50), cv2.FONT_HERSHEY_PLAIN, 2, (95, 69, 235), 4)

            (widthTxt2, heightTxt2), baseline = cv2.getTextSize(result, cv2.FONT_HERSHEY_PLAIN, 2, 4)
            x = (widthWin - widthTxt2) // 2
            cv2.putText(img, result, (x, 450), cv2.FONT_HERSHEY_PLAIN, 2, (233, 215, 186), 4)

        cv2.imshow('Ching Chong Cha', img)
        if cv2.waitKey(1) & 0xFF == ord('r'):
            startGame = True
            stateResult = False
            error = False
            initialTime = time.time()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.load("Assets/Sounds/Komiku_-_12_-_Bicycle.mp3")
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1)
def painter():
    pygame.mixer.music.load("Assets/Sounds/music.wav")
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1)
    brushThickness = 10
    eraserThickness = 51
    img_counter=0
    folderPath = 'Resources/bar'
    myList = os.listdir(folderPath)
    print(myList)
    overlayList = []
    for imPath in myList:
        image = cv2.imread(f'{folderPath}/{imPath}', cv2.IMREAD_UNCHANGED)
        overlayList.append(image)
    print(len(overlayList))
    header = overlayList[1]
    drawColor = (49, 49, 255)

    cap = cv2.VideoCapture(0)
    cap.set(3, 640)
    cap.set(4, 480)
    detector = htm.handDetector(maxHands=1, detectionCon=0.85)
    xp, yp = 0, 0
    imgCanvas = np.zeros((480, 640, 3), np.uint8)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = detector.findHands(img, draw=False)
        lmList = detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            # print(lmList)
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]

            fingers = detector.fingersUp()
            # print(fingers)

            if fingers[1] and fingers[2]:
                print("Selection Mode")
                if y1 < 61 or y2 < 61:
                    if 20 < x1 < 67 or 20 < x2 < 67:
                        header = overlayList[0]
                        drawColor = (0, 0, 0)
                    elif 129 < x1 < 174 or 129 < x2 < 174:
                        header = overlayList[1]
                        drawColor = (49, 49, 255, 0.5)
                    elif 202 < x1 < 247 or 202 < x2 < 247:
                        header = overlayList[2]
                        drawColor = (77, 145, 255)
                    elif 275 < x1 < 320 or 275 < x2 < 320:
                        header = overlayList[3]
                        drawColor = (89, 222, 255)
                    elif 348 < x1 < 393 or 348 < x2 < 393:
                        header = overlayList[4]
                        drawColor = (99, 191, 0)
                    elif 421 < x1 < 466 or 421 < x2 < 466:
                        header = overlayList[5]
                        drawColor = (255, 182, 56)
                    elif 494 < x1 < 539 or 494 < x2 < 539:
                        header = overlayList[6]
                        drawColor = (173, 74, 0)
                    elif 567 < x1 < 612 or 567 < x2 < 612:
                        header = overlayList[7]
                        drawColor = (255, 82, 140)
                if drawColor == (0, 0, 0):
                    cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), (255, 255, 255), cv2.FILLED)
                else:
                    cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)
                xp, yp = 0, 0
            if fingers[1] and fingers[2] == False:
                if drawColor == (0, 0, 0):
                    cv2.circle(img, (x1, y1), eraserThickness // 2, (255, 255, 255), cv2.FILLED)
                else:
                    cv2.circle(img, (x1, y1), brushThickness // 2, drawColor, cv2.FILLED)
                print('Drawing Mode')
                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                if drawColor == (0, 0, 0):
                    # cv2.line(img, (xp, yp), (x1, y1), (255,255,255), eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                else:
                    # cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1

        imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
        _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
        imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
        img = cv2.bitwise_and(img, imgInv)
        img = cv2.bitwise_or(img, imgCanvas)

        img = cvzone.overlayPNG(img, header, [0, 0])
        # img-cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
        cv2.imshow('Painter', img)
        cv2.waitKey(1)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.waitKey(1) & 0xFF == ord('p'):
            img_name = "opencv_frame_{}.png".format(img_counter)
            path = os.path.abspath(os.getcwd()) + '/images_x'
            cv2.imwrite(os.path.join(path, img_name), img)
            print("{} written!".format(img_name))
            img_counter += 1
    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.load("Assets/Sounds/Komiku_-_12_-_Bicycle.mp3")
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1)
def face():
    pygame.mixer.music.load("Assets/Sounds/music.wav")
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    img_counter = 0

    def get_pr():
        properties = []  # for age,gender and race
        while not len(properties) == 3:
            try:
                ret, frame = cap.read()
                properties = []
                properties.append(DeepFace.analyze(frame, ['age']))
                properties.append(DeepFace.analyze(frame, ['gender']))
                properties.append(DeepFace.analyze(frame, ['race']))
                widthWin = frame.shape[1]
                (widthTxt, heightTxt), baseline = cv2.getTextSize(properties[2][0]['dominant_race'], cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                if - 140 + widthTxt > 0:
                    xText = widthWin - 60 - widthTxt
                else:
                    xText = widthWin - 140
            except:
                properties = []
        return properties, xText

    properties, xText = get_pr()

    while True:

        ret, frame = cap.read()
        result = DeepFace.analyze(frame, ['emotion'], False)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (128, 128, 0), 2)

        cv2.putText(frame, properties[1][0]['dominant_gender'], (500, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (110, 0, 214), 2, cv2.LINE_4)
        cv2.putText(frame, result[0]['dominant_emotion'], (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 215, 255), 2, cv2.LINE_4)
        cv2.putText(frame, str(properties[0][0]['age']), (500, 120), cv2.FONT_HERSHEY_SIMPLEX, 1, (110, 0, 214), 2, cv2.LINE_4)
        cv2.putText(frame, properties[2][0]['dominant_race'], (xText, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (110, 0, 214), 2, cv2.LINE_4)

        cv2.imshow('Demo video', frame)
        if cv2.waitKey(1) & 0xFF == ord('n'):
            properties, xText = get_pr()
        if cv2.waitKey(1) & 0xFF == ord('p'):
            img_name = "opencv_frame_{}.png".format(img_counter)
            path = os.path.abspath(os.getcwd()) + '/images_x'
            cv2.imwrite(os.path.join(path, img_name), frame)
            print("{} written!".format(img_name))
            img_counter += 1


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    pygame.mixer.music.load("Assets/Sounds/Komiku_-_12_-_Bicycle.mp3")
    pygame.mixer.music.set_volume(MUSIC_VOLUME)
    pygame.mixer.music.play(-1)


class Menu:
    def __init__(self, surface):
        self.surface = surface
        self.background = Background(background_image='background_menu.jpg')
        self.click_sound = pygame.mixer.Sound(f"Assets/Sounds/slap.wav")


    def draw(self):
        self.background.draw(self.surface)
        # draw title
        infoObject = pygame.display.Info()
        ui.draw_text(self.surface, GAME_TITLE, (infoObject.current_w//2, 120), COLORS["title"], font=FONTS["big"],
                    shadow=True, shadow_color=(255,255,255), pos_mode="center")


    def update(self):
        self.draw()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return "menu"
        if ui.button(self.surface, 250, "Underwater Hunting", click_sound=self.click_sound):
            return "game"
        if ui.button(self.surface, 330, "Ching Chong Cha", click_sound=self.click_sound):
            rock()
            # return "rock"
        if ui.button(self.surface, 410, "Visual Paint", click_sound=self.click_sound):
            painter()
            # return "painter"
        if ui.button(self.surface, 490, "Face Detector", click_sound=self.click_sound):
            face()
            # return "face"

        if ui.button(self.surface, 500+BUTTONS_SIZES[1]*1.5, "Quit", click_sound=self.click_sound):
            pygame.quit()
            sys.exit()
