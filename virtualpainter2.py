import cv2
import numpy as np
import time
import os
import handtrackingmodule2 as htm

brushThickness = 20
eraserThickness = 100

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Directory for header images
folderPath = os.path.join(script_dir, "header")

myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(os.path.join(folderPath, imPath))
    overlayList.append(image)

print(len(overlayList))

header = overlayList[0]

drawColor = (255, 0, 0)

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = htm.HandDetectorMP(detection_con=0.85)

# Initial points
xp, yp = 0, 0

imgCanvas = np.zeros((720, 1280, 3), np.uint8)

save_canvas = False  # Flag to determine whether to save the canvas

while True:
    # Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Find hand landmarks
    img = detector.find_hands(img)
    lm_list = detector.find_position(img, draw=True)

    if len(lm_list) != 0:
        # Tip of index and middle finger
        x1, y1 = lm_list[8][1:]
        x2, y2 = lm_list[12][1:]

        # Check which fingers are up
        fingers = detector.fingers_up()
        print(fingers)

        # Check if thumb and pinky finger are up for saving canvas
        if len(fingers) >= 5:  # Ensure fingers list has enough elements
            if fingers[0] and not fingers[4]:
                print("Thumb up")
                save_canvas = True
            elif not fingers[0] and fingers[4]:
                print("Pinky up")
                save_canvas = False

        # Check if 2 fingers are up (selection mode)
        if len(fingers) >= 3:  # Ensure fingers list has enough elements
            if fingers[1] and fingers[2]:
                print("Selection Mode")
                xp, yp = 0, 0

                # Clicking the header
                if y1 < 125:
                    if 200 < x1 < 400:
                        header = overlayList[0]
                        drawColor = (255, 0, 0)
                    elif 500 < x1 < 700:
                        header = overlayList[1]
                        drawColor = (0, 0, 255)
                    elif 750 < x1 < 900:
                        header = overlayList[2]
                        drawColor = (0, 255, 0)
                    elif 1000 < x1 < 1150:
                        header = overlayList[3]
                        drawColor = (0, 0, 0)
                    elif 1250 < x1 < 1450:
                        header = overlayList[4]
                        if save_canvas:
                            canvas_folder = os.path.join(script_dir, "canvas")
                            if not os.path.exists(canvas_folder):
                                os.makedirs(canvas_folder)
                            cv2.imwrite(os.path.join(canvas_folder, "canvas.png"), imgCanvas)
                            save_canvas = False
                            print("Canvas saved!")
                            # Prompt box
                            cv2.rectangle(img, (400, 200), (880, 400), (0, 255, 0), cv2.FILLED)
                            cv2.putText(img, "Canvas Saved!", (420, 340), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 5, cv2.LINE_AA)

                cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # Only index finger is up aka (drawing mode)
        if len(fingers) >= 3:  # Ensure fingers list has enough elements
            if fingers[1] and not fingers[2]:
                print("Drawing mode")

                if xp == 0 and yp == 0:
                    xp, yp = x1, y1

                if drawColor == (0, 0, 0):
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
                else:
                    cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                    cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

                xp, yp = x1, y1

    # Create mask and combine images
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # Overlay the header
    resizedHeader = cv2.resize(header, (1280, 125))
    img[0:125, 0:1280] = resizedHeader

    # Show images
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)

    # Wait for key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
