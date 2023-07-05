import cv2
import numpy as np
import pytesseract
import time

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

count = 0
paused = False
click_start = None
click_end = None
start_mouse_tracking = False
crop_img = False

def on_mouse(event, x, y, flags, param):
    global click_start, click_end, start_mouse_tracking
    if start_mouse_tracking and event == cv2.EVENT_LBUTTONDOWN:
        click_start = (x, y)
    elif start_mouse_tracking and event == cv2.EVENT_LBUTTONUP:
        click_end = (x, y)

cap = cv2.VideoCapture(0)
cv2.namedWindow('Edges')
cv2.setMouseCallback('Edges', on_mouse)

while True:
    key = cv2.waitKey(1)
    count += 1
    _, frame = cap.read()

    if not paused:
        edges = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([30, 150, 50])
        upper_red = np.array([255, 255, 180])
        mask = cv2.inRange(hsv, lower_red, upper_red)
        res = cv2.bitwise_and(frame, frame, mask=mask)
        edges = cv2.Canny(frame, 100, 200)
        """
        if crop_img == True:
            crop = edges[start_point[1]:end_point[1], start_point[0]:end_point[0]]
            print(pytesseract.image_to_string(crop, lang='eng',config='--psm 6'))
            cv2.imshow('Edges', crop)
        else:
            cv2.imshow('Edges', edges)
        
    
        #print(edges.shape)


    # Start mouse tracking when "[" key is pressed
    if key == ord('['):
        paused = not paused
        start_mouse_tracking = not start_mouse_tracking

    if key == ord('b'):
        if not paused:
            crop_img = False

    # Draw rectangle if click_start and click_end are available and video is paused
    if paused and click_start is not None and click_end is not None:
        image = edges.copy()
        start_point = click_start
        end_point = click_end
        color = (255, 0, 0)
        thickness = 2
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
        crop_img = True
        #crop_img = image[start_point[1]:end_point[1], start_point[0]:end_point[0]]
        cv2.imshow('Edges', image)

    if click_start is not None and click_end is not None:
        print("Mouse click start:", click_start)
        print("Mouse click end:", click_end)
        click_start = None
        click_end = None
    
    # Wait for Esc key to stop
    if key == 27:
        break
    #time.sleep(1)

cv2.destroyAllWindows()
cap.release()

print("Total frames processed:", count)
