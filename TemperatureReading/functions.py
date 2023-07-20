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
    
def create_csv_file(file_path):
    filename = 'data.csv'  # Specify the name of the CSV file
    
    # Check if the file already exists
    if os.path.exists(filename):
        print(f"File '{filename}' already exists.")
        return
    
    # Open the file in write mode
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
"""
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
"""