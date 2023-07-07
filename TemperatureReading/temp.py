import cv2
import numpy as np
import pytesseract
import time
import datetime as dt
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def on_mouse(event, x, y, click_start, click_end):
    if start_mouse_tracking and event == cv2.EVENT_LBUTTONDOWN:
        click_start = (x, y)
    elif start_mouse_tracking and event == cv2.EVENT_LBUTTONUP:
        click_end = (x, y)

def animate(i, xs, ys, count,data, paused, click_start, click_end, start_mouse_tracking, crop_img, duration, start):
    _, frame = cap.read()
    key = cv2.waitKey(1)
    count += 1 
    edges = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    print(paused)
    if not paused:
        if crop_img == True:
            start_time = time.time()

            crop = edges[start_point[1]:end_point[1], start_point[0]:end_point[0]]
            cv2.imshow('Edges', crop)
            
            # Extract the text from the cropped image
            temp = pytesseract.image_to_string(crop, lang='eng', config='--psm 6').replace('\n', '')
            
            xs.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
            ys.append(temp)
            xs = xs[-20:]
            ys = ys[-20:]
            
            ax.clear()
            ax.plot(xs, ys)
            
            plt.xticks(rotation=45, ha='right')
            plt.subplots_adjust(bottom=0.30)
            plt.title('Temperature over Time')
            plt.ylabel('Temperature (deg C)')
            
            # Append the data to the list
            data.append([time.ctime(start_time), temp])
            with open(os.path.join(current_dir, 'data.csv'), 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Timestamp', 'Temp'])
                writer.writerows(data)
            print(temp)
            print('Current Time:', time.ctime(time.time()))
            
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
        cv2.setMouseCallback("Edges", on_mouse, click_start, click_end)
        image = edges.copy()
        start_point = click_start
        end_point = click_end
        color = (255, 0, 0)
        thickness = 2
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
        # Crops it
        crop_img = True
        cv2.imshow('Edges', image)
    
    if click_start is not None and click_end is not None:
        print("Mouse click start:", click_start)
        print("Mouse click end:", click_end)
        click_start = None
        click_end = None

if __name__ == '__main__':
    #global count, data, paused, crop_img, duration, start, click_start, click_end, start_mouse_tracking
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    xs = []
    ys = []

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    current_dir = os.getcwd()

    count = 0
    data = []
    paused = False
    click_start = None
    click_end = None
    start_mouse_tracking = False
    crop_img = False
    duration = 180
    start = True

    


    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cv2.namedWindow('Edges')
    cv2.setMouseCallback('Edges', on_mouse)
    
    ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys, count, data, paused, click_start, click_end, start_mouse_tracking, crop_img, duration, start), interval=1)
    
    plt.show()
    
    cv2.destroyAllWindows()
    cap.release()
    
    print("Total frames processed:", count)
