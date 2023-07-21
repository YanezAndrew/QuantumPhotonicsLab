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

def single_IV_sweep(keysight=None, channel=1, start=0, stop=10, points=10, aper=1E-4, current_compliance=0.1):
    '''
        Remember to connect, initialze keysight and import numpy before executing this function!
        Runs an IV measurement on Channel 1.
        Return a numpy array with the current values.
    '''

    # Source
    keysight.write("*RST")
    #keysight.write(":SOUR:FUNC:MODE VOLT")
    keysight.write(":SOUR:VOLT:MODE SWE")
    #keysight.write(":SOUR:VOLT:RANG:AUTO:LLIM 0.002")
    keysight.write(":SOUR:VOLT:STAR " + str(start))
    keysight.write(":SOUR:VOLT:STOP " + str(stop))
    keysight.write(":SOUR:VOLT:POIN " + str(points))

    # Sense
    keysight.write(":SENSE:FUNC ""CURR""")
    #keysight.write(":SENSE:CURR:RANG:AUTO OFF")
    #keysight.write(":SENSE:CURR:RANG 1E-9")
    keysight.write(":SENSE:CURR:APER " + str(aper))
    keysight.write(":SENSE:CURR:PROT " + str(current_compliance))
    # keysight.write(":SENSE:CURR:RANG:AUTO:LLIM 1E-9") # 1nA

    # Trigger
    keysight.write(":TRIG:SOUR AINT")
    keysight.write(":TRIG:COUN " + str(points))

    # measurement
    keysight.write(":OUTP" + str(channel) + " ON")
    keysight.write(":INIT (@" + str(channel) + ")")
    keysight.write(":FETC:ARR:CURR? (@" + str(channel) + ")")
    data = keysight.read()
    keysight.write(":OUTP" + str(channel) + " OFF")


    # data convertion
    l = data.split(',')
    current_list = np.zeros(points, dtype=np.float64)
    for i in range(points):
        current_list[i] = float(l[i])

    return current_list

def intialize_device():
    keysight_usb_id = 'USB0::0x0957::0x8C18::MY51145486::INSTR'
    rm = pv.ResourceManager()
    print(rm)
    print(rm.list_resources())
    try:
        keysight = rm.open_resource(keysight_usb_id) # open Keysight according to the usb id of keysight that comes along with it.
    except:
        print("Failed to connect to Keysight. Please check your connection")
        exit(1)
    '''
    code for testing if keysight is connected successfully
    '''
    print(keysight)
    print(keysight.query('*IDN?')) # return ID information
    keysight.write('*RST') # to reset all setup on the keysight
    time.sleep(0.1)   



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

    count = 0
    data = []
    paused = False
    click_start = None
    click_end = None
    start_mouse_tracking = False
    crop_img = False
    duration = 60
    start = True
    start_time = None


    intialize_device()
    start = -1
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
                crop = edges[start_point[1]:end_point[1], start_point[0]:end_point[0]]
                if start_time is None:  # Check if start_time is not set
                    start_time = time.time()
                cv2.imshow('Edges', crop)
                if time.time() - start_time >= duration:

                    ###########
                    M = np.zeros((10, points))
                    for i in range(10):
                        M[i] = single_IV_sweep(keysight, 1, start, stop, points, current_compliance=2e-4)
                    print(M)
                    ###########
                    

                    # Extract the text from the cropped image
                    temp = (pytesseract.image_to_string(crop, lang='eng', config='--psm 6'))
                    temp = temp.replace('\n', '')
                    # Append the data to the list
                    data.append([time.ctime(start_time), temp])
                    print(temp)
                    print('Current Time:', time.ctime(time.time()))
                    start_time = None
                    with open(file_path, 'w', newline='') as csvfile:
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
