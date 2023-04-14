import random
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time
import streamlit as st

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, Player]

# Define the Streamlit app
st.title("Rock Paper Scissors Game")
start_button = st.button("Start Game")

# Create a Streamlit image frame to display the game
stframe = st.empty()
initialTime = 0
# if start_button:
#         startGame = True
#         initialTime = time.time()
#         stateResult = False
while True:
    if start_button:
        startGame = True
        initialTime = time.time()
        stateResult = False
        start_button = False
    imgBG = cv2.imread("BG.png")
    success, img = cap.read()

    imgScaled = cv2.resize(img, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]

    # Find Hands
    hands, img = detector.findHands(imgScaled)  # with draw
    
    if startGame:
        
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_PLAIN, 6, (255, 0, 255), 4)

            if timer > 3:
                stateResult = True
                timer = 0

                if hands:
                    playerMove = None
                    hand = hands[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMove = 1
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMove = 2
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMove = 3

                    randomNumber = random.randint(1, 3)
                    imgAI = cv2.imread(f'{randomNumber}.png', cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))

                    # Player Wins
                    if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1

                    # AI Wins
                    if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1
                    # Draw
                    if (playerMove == 3 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 2) or \
                            (playerMove == 1 and randomNumber == 1):
                        scores[0] += 1
                        scores[1] += 1

    imgBG[234:654, 795:1195] = imgScaled

    if stateResult:
        imgBG = cvzone.overlayPNG(imgBG, imgAI, (149, 310))
    if scores[0]!=0 or scores[1]!=0:
        cv2.putText(imgBG, 'Win' if scores[0]>scores[1] else 'Draw' if scores[0]==scores[1] else 'Lose', (315, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
        cv2.putText(imgBG, 'Win' if scores[1]>scores[0] else 'Draw' if scores[0]==scores[1] else 'Lose', (1020, 215), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 6)
    
    # Display the image in Streamlit
    stframe.image(cv2.cvtColor(imgBG, cv2.COLOR_BGR2RGB), channels="RGB")
