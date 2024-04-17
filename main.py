import cv2
import os


width,height=1280,720
folderPath="presentation"


cap=cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)


#getimages
pathImages=os.listdir(folderPath)

print (pathImages)


while True:
    success, img=cap.read()
    cv2.imshow("Image",img)
    key=cv2.waitKey(1)

    if key==ord('q'):
        break

    