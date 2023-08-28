import cv2
import numpy as np
import pytesseract
import time
import csv
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pyvisa as pv
from matplotlib import style
import time
from datetime import datetime
import pandas as pd
from scipy.optimize import curve_fit
import re

def on_mouse(event, x, y, flags, param):
    """
        Global Variables:
            click_start = (x, y)
            click_end = (x, y)

        Tracks the point at which left mouse button is clicked
        and the point at which it is released.
    """
    global click_start, click_end, start_mouse_tracking
    if start_mouse_tracking and event == cv2.EVENT_LBUTTONDOWN:
        click_start = (x, y)
        print("Mouse click start:", click_start)
    elif start_mouse_tracking and event == cv2.EVENT_LBUTTONUP:
        click_end = (x, y)
        print("Mouse click end:", click_end)
def key_press(key):
    """
        Variable:
            key

        Each key has a specific action

        Esc (27) - stops
        Space Bar (32) - pauses
        b - resizes window back to original

    """
    # Wait for Esc key to stop
    if key == 27:
        return "Escape"
    # Start mouse tracking when "Space Bar" key is pressed
    if key == 32:
        return "Space Bar"
    # Resize
    if key == ord('b'):
        return 'B'
    
def create_csv_file(file_path):
    """
        Variable:
            file_path
        
        Creates a csv file if there isn't one with the same name

    """
    
    # Check if the file already exists
    if os.path.exists(file_path):
        print(f"File '{file_path}' already exists.")
        return
    
    # Open the file in write mode
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

def single_IV_sweep(keysight=None, channel=1, start=0, stop=10, points=10, aper=1E-4, current_compliance = 5e-3):
     # Source
    keysight.write("*RST")

    keysight.write(":SOUR:FUNC:MODE VOLT")
    keysight.write(":SOUR:VOLT:MODE SWE")
    keysight.write(":SOUR:VOLT:STAR " + str(start))
    keysight.write(":SOUR:VOLT:STOP " + str(stop))
    keysight.write(":SOUR:VOLT:POIN " + str(points))
    # Sense
    keysight.write(":SENSE:FUNC ""CURR""")
    keysight.write(":SENSE:CURR:APER 1e-4")
    keysight.write(":SENSE:CURR:PROT " + str(current_compliance))

    # Automatic Trigger
    keysight.write(":TRIG:SOUR AINT")
    keysight.write(":TRIG:COUN " + str(points))
    

    # measurement
    keysight.write(":OUTP" + str(channel) + " ON")
    keysight.write(":INIT (@" + str(channel) + ")")
    keysight.write(":FETC:ARR:CURR? (@" + str(channel) + ")")
    data = keysight.read()
    #print("data: ", data)
    keysight.write(":OUTP" + str(channel) + " OFF")

    # Data Conversion to List of Voltages
    l = data.split(',')
    current_list = np.zeros(points, dtype=np.float64)
    for i in range(points):
        current_list[i] = float(l[i])
    keysight.clear()
    return current_list

def intialize_device():
    rm = pv.ResourceManager()
    #print(rm.list_resources())
    #print(rm)
    keysight_USB_ID= rm.list_resources()[0]
    #keysight_USB_ID = "USB0::2391::35864::MY51145486::0::INSTR"
    try:
        keysight = rm.open_resource(keysight_USB_ID) # open Keysight according to the usb id of keysight that comes along with it.
    except:
        print("Failed to connect to Keysight. Please check your connection")
        exit(1)
  
    # Set Timeout or Else Program could crash 25 sec
    keysight.timeout = 25000
    print(keysight.query('*IDN?'))
    keysight.clear()
    return keysight

def func(x, m, b):
    """
        Curve fits a linear line using the equation y = mx + b
    """
    return m * x + b

def is_float(value):
    """
        Checks if value is a valid float.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    # Opens the .exe file to convert photo into python float
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    keysight = intialize_device()
    
    # Find Correct Directory QuantumPhotonicsLab\TemperatureReading\Data
    current_dir = os.getcwd()
    lab_index = current_dir.find("QuantumPhotonicsLab")
    partial_path = current_dir[:lab_index + len("QuantumPhotonicsLab")]
    current_dir = f"{partial_path}\TemperatureReading\Data"
    print(current_dir)

    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Initialize CSV count
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

    # Initialize Variables 
    reading_count = 0
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
    error_cnt = 0

    # Voltage Range and Points
    start = 2
    stop = -8
    points = 1500

    #,cv2.CAP_DSHOW (Take Off for Mac)
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    cap.set(3, 1280) # set the resolution
    cap.set(4, 720)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 0)
    cv2.namedWindow('Edges')
    cv2.setMouseCallback('Edges', on_mouse)
    fig, ax = plt.subplots()
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
                slope_crop = (end_point[1] - start_point[1]) / (end_point[0] - start_point[0])
                x_1 = start_point[0]
                x_2 = end_point[0]
                y_1 = start_point[1]
                y_2 = end_point[1]
                if (slope_crop < 0):
                    y_1 = end_point[1]
                    y_2 = start_point[1]
                crop = edges[y_1:y_2, x_1:x_2]
                cv2.imshow('Edges', crop)
                if start_time == None:
                    start_time = time.time()
                if time.time() - start_time >= duration or reading_count == 0:
                    print(reading_count)
                    reading_count +=1
                    ###########
                    M = np.zeros((10, points))
                    for i in range(10):
                        M[i] = single_IV_sweep(keysight, 1, start, stop, points, 1E-4, 5e-3)
                        keysight.close()
                        keysight = intialize_device()

                    x = list(np.linspace(start, stop, points))
                    y = list(np.mean(M, axis=0))
                    params, covariance = curve_fit(func, x, y)
                    m_fit, c_fit = params
                    slope = m_fit
                    # resistance is Volts / Amps
                    resistance = 1 / slope
                    ###########


                    # Extract the text from the cropped image
                    temp = (pytesseract.image_to_string(crop, lang='eng', config='--psm 6')).replace('\n', '')
                    temp = re.sub(r'[^0-9.]', '', temp)
                    temp = re.sub(r'\.(?=.*\.)', '', temp)
                    if not is_float(temp):
                        image_filename = os.path.join("error/", f"ERROR_{current_date}_ ({error_cnt}).jpg")
                        cv2.imwrite(image_filename, crop)
                        error_cnt += 1
                    else:
                        temp = float(temp)
                        temp = "{:.3f}".format(temp)
                    
                    plt.scatter(x, y, s=6)
                    plt.pause(0.01)  # Pause for 0.01 seconds to show each step

                    # Append the data to the list
                    data.append([time.ctime(start_time), temp, x, y, resistance])
                    df = pd.DataFrame(data, columns=['Time', 'Temperature', 'Voltage','Amps', 'Resistance'])
                    df.to_csv(file_path, index=False)
                    print(temp, resistance)
                    print('Current Time:', time.ctime(time.time()))
                    # Reset Time
                    start_time = None
                    print(df['Temperature'])
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
            color = (0, 0, 255)
            thickness = 2
            image = cv2.rectangle(cv2.cvtColor(image, cv2.COLOR_BGR2RGB), click_start, click_end, color, thickness)
            crop_img = True
            cv2.imshow('Edges', image)
        if click_start is not None and click_end is not None:
            click_start = None
            click_end = None

    keysight.close()
    plt.title("I-V")
    plt.xlabel('Voltage (V)')
    plt.ylabel('Current (A)')
    plt.show()
    cap.release()
    cv2.destroyAllWindows()
    print("Total frames processed:", count)
