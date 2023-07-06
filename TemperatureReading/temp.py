import cv2
import numpy as np
import pytesseract
import time
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time

#this is a test
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

current_dir = os.getcwd()

count = 0
data = []
paused = False
click_start = None
click_end = None
start_mouse_tracking = False
crop_img = False
duration = 5 
start = True

def on_mouse(event, x, y, flags, param):
    global click_start, click_end, start_mouse_tracking
    if start_mouse_tracking and event == cv2.EVENT_LBUTTONDOWN:
        click_start = (x, y)
    elif start_mouse_tracking and event == cv2.EVENT_LBUTTONUP:
        click_end = (x, y)


#,cv2.CAP_DSHOW
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cv2.namedWindow('Edges')
cv2.setMouseCallback('Edges', on_mouse)

while start:
    _, frame = cap.read()
    key = cv2.waitKey(1)
    count += 1 
    edges = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if not paused:
        if crop_img == True:
            start_time = time.time()
            
            #Crops it
            crop = edges[start_point[1]:end_point[1], start_point[0]:end_point[0]]
            cv2.imshow('Edges', crop)

            # Extract the text from the cropped image
            temp = (pytesseract.image_to_string(crop, lang='eng', config='--psm 6'))
            temp = temp.replace('\n', '')
            # Append the data to the list
            data.append([time.ctime(start_time), temp])
            with open(os.path.join(current_dir, 'data.csv'), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Timestamp', 'Temp'])
                writer.writerows(data)
            print(temp)
            print('Current Time:', time.ctime(time.time()))
            #print(time.ctime(start_time))

            elapsed_time = 0  # Initialize elapsed time to zero
            while elapsed_time < duration:
                time.sleep(1)  # Delay 1 second
                elapsed_time += 1  # Increment the elapsed time by 1 second
                print(elapsed_time)
                if cv2.waitKey(1) == ord('b'):
                    crop_img = False
                    break 
        else:
            cv2.imshow('Edges', edges)


    # Start mouse tracking when "Space Bar" key is pressed
    if key == 32:
        paused = not paused
        start_mouse_tracking = not start_mouse_tracking
        print("Paused: ", paused)

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
        cv2.imshow('Edges', image)
    

    if click_start is not None and click_end is not None:
        print("Mouse click start:", click_start)
        print("Mouse click end:", click_end)
        click_start = None
        click_end = None
    
    # Wait for Esc key to stop
    if key == 27:
        break

cv2.destroyAllWindows()
cap.release()
 
print("Total frames processed:", count)


# Set the figure size
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

# Make a list of columns
columns = ['Timestamp', 'Temp']

# Read a CSV file
df = pd.read_csv("data.csv", usecols=columns)

# Convert 'Timestamp' column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format="%a %b %d %H:%M:%S %Y")

# Plot the points on the line
plt.plot(df['Timestamp'], df['Temp'], '-o')

plt.show()