import numpy as np
import time


def move_right(x_list, increment):
    #print(len(x_list))
    #axis_x.move_by(increment)
    print(" *" * len(x_list))

# , axis_x)

def move_left(x_list, steps, increment):
    #axis_x.move_by(-1 * increment)
    spaces = len(x_list) 
    stars = steps - spaces
    # print(x)
    # print(spaces)
    print("  " * (spaces), "* " * stars)











code_type = 0
enable_background = 1
serialNumber = 2108112774
center_wavelength = 780     #nm
v_res = 1       # voltage spacing of the piezo
increment = (10 ** -4) # 1 volt is around 100nm
v_range =5  # total voltage movement of the piezo
t_exp = 0.5     # exposure time in seconds
x_step_range = v_range/v_res
y_step_range = v_range/v_res
ROI_y_origin = 98
ROI_y_height = 17



# Starting the double piezo loop, within each loop a frame capture event occurs
# Note that we are doing a an intermittent reverse loop. Loop v_y changes direction
# each time it does a loop. We don't want the piezos to do large movement when each row is changed
# x and y are the global variables that denote the pixel location in the final PL picture
# ----------------------------------------------------- START
x = 0
y = 0
v_x=0
v_y=0
PL_plot = np.zeros((int(x_step_range),int(y_step_range)))
print(x_step_range)
for v_x in np.arange(0, v_range, v_res):
    x= int(v_x/v_res)
    #axis_x.move_to(v_x * increment)
    print("MOVING X")
    time.sleep(0.3)
    #time.sleep(0.3)
    # Read_X(hdl)
    # Read_Y(hdl)
    if v_y == 0:
        for v_y in np.arange(0, v_range, v_res):
            y = int(v_y/v_res)
            #axis_y.move_to(v_y * increment)
            #time.sleep(0.3)
            # Read_X(hdl)
            # Read_Y(hdl)
            print("we are in position ", x, y)
            print("MOVING Y")
            time.sleep(0.3)
            #AcquireMoveAndLock(baseFilename)
            #time.sleep(0.8)
            #time.sleep(t_exp)
    elif v_y == v_range - v_res:
        for v_y in reversed(np.arange(0, v_range, v_res)):
            y = int(v_y/v_res)
            #axis_y.move_to(v_y * increment)
            #time.sleep(0.3)
            # Read_X(hdl)
            # Read_Y(hdl)
            print("we are in position ", x, y)
            print("MOVING Y")
            time.sleep(0.3)
            #AcquireMoveAndLock(baseFilename)
            #time.sleep(t_exp)
            #time.sleep(0.8)
    else:
        print("an error has occured in movement of stage")
        print("last scanned position was pixel", x,y)
        exit()
print("PL Map completed, application will save and abort")