from newportESP302 import ESP
import sys
import math
import time


def get_increment(x_size):
    increment = float(input("Enter How Precise the movement should be: "))
    is_whole_number = (x_size / increment) % 1 == 0
    if (is_whole_number == True):
        print("Correct Increment Size")
        return increment
    else:
        print("Increment Size Won't Be Equal Across the Chip")
        get_increment(x_size)

def check_alignment():
    """
    Returns bool (True or False)


    I need to figure out a way to check aligment before just sending the laser in at the Quantum Dot

    """

def move_right(x_list):
    #print(len(x_list))
    print(" *" * len(x_list))

def move_left(x_list, steps):
    spaces = len(x_list) 
    stars = steps - spaces
    # print(x)
    # print(spaces)
    
    print("  " * (spaces), "* " * stars)




def sweep(x_list, x, y, increment):
    """

    Sweeps The Laser Through the Grid In a Snake Like Motion
            * *
    * * * * * *


    """
    #esp.move_to(0)
    y_coord = 0
    print("STEPS: ", steps)
    right = True
    left = False
    curr_value = 0
    while(y_coord != y):
        if (left):
            if len(x_list) == 0:
                y_coord +=1
                right = True
                left = False
                curr_value = 0
                continue
            curr_value = x_list.pop()
            move_left(x_list, steps)
        elif (right):
            if (len(x_list) == steps):
                y_coord +=1
                left = True
                right = False
                continue
            curr_value += increment
            x_list.append((round(curr_value, 1)))
            move_right(x_list)
            

        

if __name__ == '__main__':
    # Checks if Device is Connected
    # try:
    #     esp = ESP('/dev/ttyUSB0')  
    #     axis1 = esp.axis(1)
    #     print("ESP is initialized successfully!")
    # except Exception as e:
    #     print("ESP initialization failed:", e, "\n\n\n")
    #     sys.exit(1)
    x_list = []

    x = int(input("Enter Max X coord (mm): "))
    y = int(input("Enter Max Y coord (mm): "))

    #
    # Gets Increment Size Needed
    #
    increment = get_increment(x)

    steps = int(x / increment)

    start_sweep = False

    start_sweep = input("Type 1 if Ready to Start Sweep and 0 if not ready:")



    if (start_sweep == '1'):
        # esp
        sweep(x_list, x, y, increment)

    print(x_list)
    print(len(x_list))

    #while(len(x_axis) != )