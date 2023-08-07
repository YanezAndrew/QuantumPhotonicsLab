from ethernet_newport import ESP
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import sys
import math
import time

def customize_plot(ax, x_steps, y_steps, padding = 0.2):
    ax.set_xlim(-padding, x_steps + padding -1)
    ax.set_ylim(-padding, y_steps + padding -1)
    ax.set_xticks(range(x_steps))
    ax.set_yticks(range(y_steps))
    ax.grid(True)
    ax.set_xlabel('X Position')
    ax.set_ylabel('Y Position')
    ax.set_title('Sweep Motion Visualization')
    
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
def move_right(x_list, increment):
    #print(len(x_list))
    axis_x.move_by(increment)
    print(" *" * len(x_list))

# , axis_x)

def move_left(x_list, steps, increment):
    axis_x.move_by(-1 * increment)
    spaces = len(x_list) 
    stars = steps - spaces
    # print(x)
    # print(spaces)
    print("  " * (spaces), "* " * stars)



#
# , axis_x, axis_y)
#
def sweep(x_list, y_list, x_max, y_max, x_steps, y_steps, increment, axis_x, axis_y):
    """

    Sweeps The Laser Through the Grid In a Snake Like Motion
            * *
    * * * * * *


    There are two lists running here:
        x_list
        y_list
    x_list: 
        Right:
            has the point it will shoot the laser appended to the top of the list
        Left:
            has the point is about to move appended from the list
    y_list:
        has the point it will move to appended to the top

    
    """
    # axis_x.move_to(0) This is to move to (0,0)
    # axis_y.move_to(1) This is to move to (0,0)
    print("X STEPS: ", x_steps)
    print("Y STEPS: ", y_steps)
    right = True
    left = False
    curr_value = 0.0


    fig, ax = plt.subplots()
    customize_plot(ax, x_steps, y_steps)
    y_list.append(0.0)



    while(len(y_list) -1 != y_steps):
        #print("Y: ", len(y_list) -1)
        if (left):
            if len(x_list) == 0:
                y_list.append(round(y_list[-1] + increment, 1))
                axis_y.move_by(increment)
                right = True
                left = False
                curr_value = 0.0
                continue
            x = len(x_list) - 1
            y = len(y_list) - 1
            #print(x, y)
            curr_value = x_list.pop()

            #
            #
            move_left(x_list, x_steps, increment)
            #
            #
            plt.scatter(x, y, color='blue', marker='o')
        elif (right):
            if (len(x_list) == x_steps):
                y_list.append(y_list[-1] + increment)
                axis_y.move_by(increment)
                left = True
                right = False
                continue
            x_list.append((round(curr_value, 1)))
            x = len(x_list) - 1
            y = len(y_list) - 1
            #print(x, y)

            curr_value += increment
            # Shoot Laser and then Move
            #
            move_right(x_list, increment)
            #
            #
            plt.scatter(x, y, color='blue', marker='o')

        plt.pause(0.01)  # Pause for 0.01 seconds to show each step
    plt.show()
    
            
            

        

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
    device_ip = '192.168.254.254'
    device_port = 5001
    esp = ESP(device_ip, device_port)
    axis_x = esp.axis(1)
    axis_y = esp.axis(2)

    axis_x.travel_limits()
    axis_y.travel_limits()

    axis_x.backlash()
    axis_y.backlash()

    axis_x.home_search()
    axis_y.home_search()


    axis_x.move_to(0)
    axis_y.move_to(0)
    
    x_list = []
    y_list = []

    # get_x()
    x = 1.0
    # get_y()
    y = 0.5
    # get_increment()
    increment = 0.1

    x_steps = int(x / increment) + 1
    y_steps = int(y / increment) + 1

    print("Resolution: ", x_steps, " x " , y_steps)
    start_sweep = False

    start_sweep = '1'
    #input("Type 1 if Ready to Start Sweep and 0 if NOT ready:")


    
    if (start_sweep == '1'):
        # esp
        #
        #
        #

        # Create the figure and axis
        sweep(x_list, y_list, x, y, x_steps, y_steps, increment, axis_x, axis_y)
        # Set up the animation
        

    # print(x_list)
    # print(len(x_list))

    #while(len(x_axis) != )