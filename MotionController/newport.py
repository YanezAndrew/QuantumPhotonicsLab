from newportESP302 import ESP
import sys
import math
import time


def get_increment():
    increment = float(input("Enter How Precise the movement should be: "))
    return increment

def get_x():
    x = float(input("Enter Max X coord (mm): "))
    return x

def get_y():
    y = float(input("Enter Max Y coord (mm): "))
    return y

def check_alignment():
    """
    Returns bool (True or False)


    I need to figure out a way to check aligment before just sending the laser in at the Quantum Dot

    """


# , axis_x)
def move_right(x_list):
    #print(len(x_list))
    #axis_x.move_by(1)
    print(" *" * len(x_list))

# , axis_x)

def move_left(x_list, steps):
    #axis_x.move_by(1)
    spaces = len(x_list) 
    stars = steps - spaces
    # print(x)
    # print(spaces)
    print("  " * (spaces), "* " * stars)



#
# , axis_x, axis_y)
#
def sweep(x_list, x_steps, y_steps, increment):
    """

    Sweeps The Laser Through the Grid In a Snake Like Motion
            * *
    * * * * * *


    """
    # axis_x.move_to(0) This is to move to (0,0)
    # axis_y.move_to(1) This is to move to (0,0)
    y_coord = 0.0
    print("X STEPS: ", x_steps)
    print("Y STEPS: ", y_steps)
    right = True
    left = False
    curr_value = 0.0
    # while y_list is not empty
    while(y_coord != y_steps):
        #print("YCOORD: ",y_coord)
        if (left):
            if len(x_list) == 0:
                y_coord += 1
                right = True
                left = False
                curr_value = 0
                continue
            curr_value = x_list.pop()
            move_left(x_list, x_steps)
        elif (right):
            if (len(x_list) == x_steps):
                y_coord +=1
                left = True
                right = False
                continue
            x_list.append((round(curr_value, 1)))
            move_right(x_list)
            curr_value += increment
    #print("YCOORD: ",y_coord)
    
            
            

        

if __name__ == '__main__':
    # Checks if Device is Connected
    # try:
    #     esp = ESP('/dev/ttyUSB0')  
    #     axis_x = esp.axis(1)
    #     axis_y = esp.axis(2)
    #     print("ESP is initialized successfully!")
    # except Exception as e:
    #     print("ESP initialization failed:", e, "\n\n\n")
    #     sys.exit(1)
    x_list = []

    # get_x()
    x = 1.0
    # get_y()
    y = 2
    # get_increment()
    increment = 0.1

    x_steps = int(x / increment)
    y_steps = int(y / increment)


    start_sweep = False

    start_sweep = '1'
    #input("Type 1 if Ready to Start Sweep and 0 if NOT ready:")



    if (start_sweep == '1'):
        # esp
        #
        # , axis_x, axis_y)
        #
        sweep(x_list, x_steps, y_steps, increment)

    # print(x_list)
    # print(len(x_list))

    #while(len(x_axis) != )