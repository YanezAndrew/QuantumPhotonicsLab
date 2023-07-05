import cv2
import pygetwindow
import pyautogui
import numpy as np
import pytesseract
import time
count = 0
cv2.namedWindow("Edges", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Edges", 640, 480)

def crop(image, x1, y1, x2, y2):
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)
    # Crop the image to the rectangle
    cropped_image = image[y1:y2, x1:x2]


    return image

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  
# capture frames from a camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
  
  
# loop runs if capturing has been initialized
while(1):

    count +=1
    # reads frames from a camera
    ret, frame = cap.read()
    # converting BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of red color in HSV
    lower_red = np.array([30,150,50])
    upper_red = np.array([255,255,180])
    

    # create a red HSV colour boundary and threshold HSV image
    mask = cv2.inRange(hsv, lower_red, upper_red)
    # Bitwise-AND mask and original image
    res = cv2.bitwise_and(frame,frame, mask= mask)
    #cv2.imshow('Original',frame)
    edges = cv2.Canny(frame,100,200)
    cv2.imshow('Edges',edges)

    
    window = pygetwindow.getWindowsWithTitle('Edges')[0]
    x, y = pyautogui.position()

    # Get the position of the window
    window_x, window_y = window.left, window.top
    window_width, window_height = window.width, window.height

    # Check if the cursor is inside the window
    if (
        window_x <= x <= window_x + window_width
        and window_y <= y <= window_y + window_height
    ):
        # Cursor is inside the window
        relative_x = x - window_x
        relative_y = y - window_y
        print(f"Cursor position: ({relative_x}, {relative_y})")

    print(f"Window size: ({window_width}, {window_height})")





    if (pyautogui.mouseDown("left")):
        relative_x
        relative_y

        if (letgo):
            relative_x
            relative_y
            # draw rectangle
            # crop out
    # if click certain key then go back to normal size

    
    #text = pytesseract.image_to_string(edges, config='--psm 6 digits')
    #print(text)

    # Wait for Esc key to stop
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
  
  
# Close the window
cap.release()
  
# De-allocate any associated memory usage
cv2.destroyAllWindows() 

print("total: ", count)
