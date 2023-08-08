import cv2
import numpy as np
import pytesseract
import time
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyvisa as pv
from matplotlib import style
import time
from datetime import datetime
import pandas as pd
from scipy.optimize import curve_fit

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
    
def create_csv_file(file_path):
    filename = 'data.csv'  # Specify the name of the CSV file
    
    # Check if the file already exists
    if os.path.exists(filename):
        print(f"File '{filename}' already exists.")
        return
    
    # Open the file in write mode
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

def func(x, m, c):
    return m * x + c

def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
    

if __name__ == "__main__":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    current_dir = os.getcwd()
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    cnt = 0
    # File name with the current date
    file_name = f"data_{current_date} ({cnt}).csv"

    # Path to the file in the current directory
    file_path = os.path.join(current_dir, file_name)

    # Check if the file already exists
    file_exists = os.path.exists(file_path)
    
    
    # If the file already exists, add a number to the file name

    while file_exists:
        file_name = f"data_{current_date} ({cnt}).csv"
        file_path = os.path.join(current_dir, file_name)
        file_exists = os.path.exists(file_path)
        cnt += 1
    # Initialize CSV File
    create_csv_file(file_path)
    reading_count = 0
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
    error_cnt = 0

    start = 0
    stop = 1
    points = 5
    save_file = False

    #,cv2.CAP_DSHOW
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
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
                slope = (end_point[1] - start_point[1]) / (end_point[0] - start_point[0])
                x_1 = start_point[0]
                x_2 = end_point[0]
                y_1 = start_point[1]
                y_2 = end_point[1]
                if (slope < 0):
                    y_1 = end_point[1]
                    y_2 = start_point[1]

                print(start_point[1])
                print(end_point[1])
                print(slope)
                crop = edges[y_1:y_2, x_1:x_2]
                cv2.imshow('Edges', crop)
                if start_time == None:
                    start_time = time.time()
                if time.time() - start_time >= duration or reading_count == 0:
                    print(reading_count)
                    reading_count +=1
                    ###########
                    # Just For Testing
                    resistance = 1
                    ###########


                    # Extract the text from the cropped image
                    temp = (pytesseract.image_to_string(crop, lang='eng', config='--psm 6')).replace('\n', '')
                    if not is_float(temp):
                        image_filename = os.path.join("error/", f"ERROR_{current_date}_ ({error_cnt}).jpg")
                        cv2.imwrite(image_filename, edges)
                        error_cnt += 1
                        
                    # Append the data to the list
                    x = [0.0, 0.25, 0.5, 0.75, 1.0]
                    y = [2.4119e-09, 4.482385e-06, 8.970615000000001e-06, 1.3449680000000001e-05, 1.794105e-05]
                    data.append([time.ctime(start_time), temp, x, y, resistance])
                    df = pd.DataFrame(data, columns=['Time', 'Temperature', 'Voltage','Amps', 'Resistance'])
                    print(df.dtypes)
                    print(temp, resistance)
                    print('Current Time:', time.ctime(time.time()))
                    start_time = None
                    print(df['Temperature'])
                    df.to_csv(file_path, index=False)
            else:
                cv2.imshow('Edges', edges)
        if paused and click_start is not None and click_end is not None:
            image = edges.copy()
            if (click_start[0] + click_start[1] > click_end[0] + click_end[1]):
                start_point = click_end
                end_point = click_start
            else:
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
