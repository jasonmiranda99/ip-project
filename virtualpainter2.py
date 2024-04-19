import cv2
import numpy as np
import time
import os
import handtrackingmodule2 as htm

brushThickness=20
eraserThickness=100

folderPath = "D:\Elrich Miranda\Documents\Programs\ip-project\header"

myList=os.listdir(folderPath)
print(myList)
overlayList=[]

for imPath in myList:
    image=cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))

header=overlayList[0]

drawColor=(255,0,0)

cap =cv2.VideoCapture(0)
cap.set(3,1280)
cap.set(4,720)

detector=htm.HandDetectorMP(detection_con=0.85)

#initial points
xp,yp=0,0

imgCanvas=np.zeros((720,1280,3),np.uint8)


while True:

    #import image
    success, img=cap.read()



    #find hand landmarks

    img=detector.find_hands(img)
    lm_list=detector.find_position(img,draw=True)

    if len(lm_list)!=0:
        #print(lm_list)

        #tip of index and middle finger
        x1,y1=lm_list[8][1:]
        x2,y2=lm_list[12][1:]

        #check which fingers are up 
        fingers=detector.fingers_up()
        print(fingers)

        #check if 2 fingers are up  (selection mode)
        if fingers[1] and fingers[2]:
            print("Selection Mode")
            xp,yp=0,0

            #clicking the header
            if y1<125:
                if 250<x1<450:
                    header=overlayList[1]
                    drawColor=(0,0,255)

    
                elif 550<x1<750:
                    header=overlayList[2]
                    drawColor=(255,0,0)


                elif 800<x1<950:
                    header=overlayList[3]
                    drawColor=(0,255,0)

                
                elif 1050<x1<1200:
                    header=overlayList[4]
                    drawColor=(0,0,0)
            cv2.rectangle(img,(x1,y1-25),(x2,y2+25),drawColor,cv2.FILLED)
                



        #only index finger is up aka (drawing mode)
        if fingers[1] and fingers[2]==False:
            #cv2.circle(img, (x1, y1), 8, drawColor, cv2.FILLED)

            print("Drawing mode")

            if xp==0 and yp ==0:
                xp,yp=x1,y1

            if drawColor==(0,0,0):
                cv2.line(img,(xp,yp),(x1,y1),drawColor,eraserThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,eraserThickness)
            else:
                cv2.line(img,(xp,yp),(x1,y1),drawColor,brushThickness)
                cv2.line(imgCanvas,(xp,yp),(x1,y1),drawColor,brushThickness)

            xp,yp=x1,y1

    imgGray=cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv=cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img,imgInv)
    img = cv2.bitwise_or(img,imgCanvas)







    #overlaying the header
    resizedHeader = cv2.resize(header, (1280, 125))

    img[0:125,0:1280]=resizedHeader

    #img=cv2.addWeighted(img,0.5,imgCanvas,0.5)
    cv2.imshow("Image",img)
    cv2.imshow("Canvas",imgCanvas)
    cv2.waitKey(1)

