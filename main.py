import cv2
import os
from cvzone.HandTrackingModule import HandDetector

width, height = 1280, 720
folderPath = 'C:\\Users\\jason\\Documents\\VS Code Programs\\ip-project\\presentation'

# Camera setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Get images
pathImages = sorted(os.listdir(folderPath), key=len)

# Variables
imgNumber = 0
hs, ws = int(120), int(213)

#hand detector
detector=HandDetector(detectionCon=0.8,maxHands=1)

while True:
    success, img = cap.read()
    img =cv2.flip(img,1)
    pathFullImage = os.path.join(folderPath, pathImages[imgNumber])
    imgCurrent = cv2.imread(pathFullImage)

    hands,img=detector.findHands(img)


    # Resize the camera-captured image
    imgSmall = cv2.resize(img, (ws, hs))

    # Get dimensions of the presentation image
    h, w, _ = imgCurrent.shape

    # Overlay the camera-captured image onto the top-right corner of the presentation image
    imgCurrent[0:hs, w-ws:w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow("Slides", imgCurrent)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

