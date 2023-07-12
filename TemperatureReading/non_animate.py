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
from datetime import datetime


def on_mouse(event, x, y, flags, param):
    global click_start, click_end, start_mouse_tracking
    if start_mouse_tracking and event == cv2.EVENT_LBUTTONDOWN:
        click_start = (x, y)
        print("Mouse click start:", click_start)
    elif start_mouse_tracking and event == cv2.EVENT_LBUTTONUP:
        click_end = (x, y)
        print("Mouse click end:", click_end)

def key_press(key):
    # Wait for Esc key to stop
    if key == 27:
        return "Escape"
    # Start mouse tracking when "Space Bar" key is pressed
    if key == 32:
        return "Space Bar"

    if key == ord('b'):
        return 'B'

if __name__ == "__main__":
    #pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    current_dir = os.getcwd()
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # File name with the current date
    file_name = f"data_{current_date}.csv"

    # Path to the file in the current directory
    file_path = os.path.join(current_dir, file_name)

    # Check if the file already exists
    file_exists = os.path.exists(file_path)
    
    
    # If the file already exists, add a number to the file name
    cnt = 1
    while file_exists:
        file_name = f"data_{current_date} ({cnt}).csv"
        file_path = os.path.join(current_dir, file_name)
        file_exists = os.path.exists(file_path)
        cnt += 1

    count = 0
    data = []
    paused = False
    click_start = None
    click_end = None
    start_mouse_tracking = False
    crop_img = False
    duration = 5
    start = True
    start_time = None

    #,cv2.CAP_DSHOW
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('Edges')
    cv2.setMouseCallback('Edges', on_mouse)

    while True:
        key = cv2.waitKey(1)
        button = key_press(key)
        if button == "Escape":
            break
        elif button == "Space Bar":
            paused = not paused
            start_mouse_tracking = not start_mouse_tracking
            print("Paused: ", paused)
        elif button == 'B':
            if not paused:
                crop_img = False
        count += 1 
        ret, frame = cap.read()
        edges = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if not paused:
            if crop_img == True:
                if start_time is None:  # Check if start_time is not set
                    start_time = time.time()
                crop = edges[start_point[1]:end_point[1], start_point[0]:end_point[0]]
                cv2.imshow('Edges', crop)
                if time.time() - start_time >= duration:
                    # Extract the text from the cropped image
                    temp = (pytesseract.image_to_string(crop, lang='eng', config='--psm 6'))
                    temp = temp.replace('\n', '')
                    # Append the data to the list
                    data.append([time.ctime(start_time), temp])
                    print(temp)
                    print('Current Time:', time.ctime(time.time()))
                    start_time = None
                    with open(os.path.join(current_dir, file_path), 'w', newline='') as csvfile:
                        writer = csv.writer(csvfile)
                        #writer.writerow(['Timestamp', 'Temp'])
                        writer.writerows(data)
            else:
                cv2.imshow('Edges', edges)
        if paused and click_start is not None and click_end is not None:
            image = edges.copy()
            start_point = click_start
            end_point = click_end
            color = (255, 0, 0)
            thickness = 2
            image = cv2.rectangle(image, click_start, click_end, color, thickness)
            crop_img = True
            cv2.imshow('Edges', image)
        if click_start is not None and click_end is not None:
            click_start = None
            click_end = None
            

    cv2.destroyAllWindows()
    cap.release()
    
    print("Total frames processed:", count)
