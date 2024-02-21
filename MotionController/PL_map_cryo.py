# Imports and Declarations
# If running demo, comment the spectrometer existance check --> rewrite the code so it would
# automatically jumps through spectrometer codes for testing demos

# --------------------------- Declarations and Imports

import clr

# Import python sys module
import sys

# Import os module
import os
import glob
import string
from ethernet_newport import ESP
from ethernet_newport import Axis

from System.IO import *
from System.Threading import AutoResetEvent
# Import C compatible List and String
from System import String
clr.AddReference('System.Collections')
from System.Collections.Generic import List
# Import System.IO for saving and opening files
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import ctypes
import time
from datetime import datetime
from System.Runtime.InteropServices import GCHandle, GCHandleType
from matplotlib.animation import FuncAnimation

# relevant to the MDT
try:
    from MDT_COMMAND_LIB import *
except OSError as ex:
    print("Warning:", ex)

# Add needed dll references
sys.path.append(os.environ['LIGHTFIELD_ROOT'])
sys.path.append(os.environ['LIGHTFIELD_ROOT'] + "\\AddInViews")
clr.AddReference('PrincetonInstruments.LightFieldViewV5')
clr.AddReference('PrincetonInstruments.LightField.AutomationV5')
clr.AddReference('PrincetonInstruments.LightFieldAddInSupportServices')

# PI imports
from PrincetonInstruments.LightField.Automation import Automation
from PrincetonInstruments.LightField.AddIns import ExperimentSettings
from PrincetonInstruments.LightField.AddIns import CameraSettings
from PrincetonInstruments.LightField.AddIns import DeviceType
from PrincetonInstruments.LightField.AddIns import RegionOfInterest
from PrincetonInstruments.LightField.AddIns import ImageDataFormat
from PrincetonInstruments.LightField.AddIns import SpectrometerSettings

# --------------------------- Global Parameter Declarations (Modify to desired settings)
#experiment_name = "ff"
# If you are running real experiment please specify code_type = 1 else for demo
code_type = 1
enable_background = 1
serialNumber = 2108112774
center_wavelength = 780     #nm
increment = 0.002       # units of mm
originx = 18.402
originy = 20.700
range = 0.020  # units of mm
t_exp = 0.5     # exposure time in seconds
x_step_range = range/increment
y_step_range = range/increment
ROI_y_origin = 189
ROI_y_height = 44
animation_update_required = False

# Function for ESP302
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


def move_right(x_list, increment):
    # print(len(x_list))
    axis_x.move_by(increment)
    print(" *" * len(x_list))


def move_left(x_list, steps, increment):
    axis_x.move_by(-1 * increment)
    spaces = len(x_list)
    stars = steps - spaces
    # print(x)
    # print(spaces)
    print("  " * (spaces), "* " * stars)
    
# Function Definitions for the CCD and the Spectrometer
def Max_int_PLmap(incoming_data):
    global animation_update_required
    incoming_data = np.max(incoming_data)
    print("c1")
    print(PL_plot)
    PL_plot[x][y] = incoming_data
    print("c2")
    # NOT RETURNING SOMETHING FOR SOME REASON

def update_plot(frame):
    global animation_update_required

    # Your existing animation update code here
    
    if animation_update_required:
        PL_plot.set_array(np.flip(PL_plot, 0))
        animation_update_required = False

    return PL_plot,


def bg_correction(first_data_set):
    if enable_background == 1:
        if x == 0 and y == 0:
            global background_data
            background_data = first_data_set 
            print("background obtained")
        else:
            return
        return
    else:
        background_data = 0

def check_spectrometer_exist():
    if code_type == 1:
        if spec_found() == True:
            return
        else:
            print("Spectrometer not found")
            exit()
    else:
        print("Demo mode, spectrometer check skipped")
        return


def check_camera_exist():
    if (device_found() == True):
        return
    else:
        print("Camera not found")
        exit()


def PLmapcapture(new_data):
    print(np.shape(new_data))
    PLmap[x][y] = new_data
    print("t9")
    #print(PLmap)


def spec_found():
    # Find connected spectrometers device
    for device in experiment.ExperimentDevices:
        if (device.Type == DeviceType.Spectrometer):
            return True

    # If connected device is not a camera inform the user
    print("Spectrometer not found. Please add a Spectrometer and try again.")
    return False


def device_found():
    # Find connected camera device
    for device in experiment.ExperimentDevices:
        if (device.Type == DeviceType.Camera):
            return True

    # If connected device is not a camera inform the user
    print("Camera not found. Please add a camera and try again.")
    return False


def convert_buffer(net_array, image_format):
    src_hndl = GCHandle.Alloc(net_array, GCHandleType.Pinned)
    try:
        src_ptr = src_hndl.AddrOfPinnedObject().ToInt64()

        # Possible data types returned from acquisition
        if (image_format==ImageDataFormat.MonochromeUnsigned16):
            buf_type = ctypes.c_ushort*len(net_array)
        elif (image_format==ImageDataFormat.MonochromeUnsigned32):
            buf_type = ctypes.c_uint*len(net_array)
        elif (image_format==ImageDataFormat.MonochromeUnsigned32):
            buf_type = ctypes.c_float*len(net_array)

        cbuf = buf_type.from_address(src_ptr)
        resultArray = np.frombuffer(cbuf, dtype=cbuf._type_)

    # Free the handle
    finally:
        if src_hndl.IsAllocated: src_hndl.Free()
    # Make a copy of the buffer
    return np.copy(resultArray)


def ManipulateImageData(dat,buff):
    print("t5")
    im = convert_buffer(dat, buff.Format)
    print("t6")
    print(im)
    print(np.shape(im))
    im = np.reshape(im,(1, int(sensor_width)))  # this one and hundred are the size of my ROI
    print("t7")
    return im


def setROI():
    #sensorCols = experiment.GetValue(CameraSettings.SensorInformationActiveAreaWidth)
    #sensorRows = experiment.GetValue(CameraSettings.SensorInformationActiveAreaHeight)
    experiment.SetCustomRegions([RegionOfInterest(0, ROI_y_origin, sensor_width, ROI_y_height, 1, ROI_y_height)])
    print("Region of Interest was set:")
    print("ROI_y_origin", str(ROI_y_origin))
    print("ROI_y_height",str(ROI_y_height))
    print("ROI_y_binning Fully binned with sensor width set at ", sensor_width)
    #RegionofInterest(x_origin,y_origin,x_width,y_height,x_binning,y_binning)


def InitializeFilenameParams():
    experiment.SetValue(ExperimentSettings.FileNameGenerationAttachIncrement, True)
    experiment.SetValue(ExperimentSettings.FileNameGenerationIncrementNumber,1)
    experiment.SetValue(ExperimentSettings.FileNameGenerationIncrementMinimumDigits, 2)
    experiment.SetValue(ExperimentSettings.FileNameGenerationAttachDate,True)
    experiment.SetValue(ExperimentSettings.FileNameGenerationAttachTime, True)


def experiment_completed(sender, event_args):
    global animation_update_required
    print("...Acquisition Complete!)")
    #global i
    frames = event_args.ImageDataSet.Frames
    print("t1")
    #i+=frames
    buffer = event_args.ImageDataSet.GetFrame(0, frames-1) #1st ROI and most recent frame in the event
    image_data = buffer.GetData()
    data_array = ManipulateImageData(image_data, buffer)
    #print(data_array)
    #print(type(data_array))
    print("t8")
    bg_correction(data_array)
    print(data_array)
    back_ground_corrected_data =np.subtract(data_array,0.97*background_data)
    print(back_ground_corrected_data)
    animation_update_required = True
    PLmapcapture(back_ground_corrected_data)
    Max_int_PLmap(back_ground_corrected_data)
    print("t10")
    acquireCompleted.Set()
    print(np.shape(back_ground_corrected_data))
    return np.copy(back_ground_corrected_data)


def device_found():
    # Find connected device.
    for device in experiment.ExperimentDevices:
        if (device.Type == DeviceType.Camera):
            return True

    # If connected device is not a camera inform the user
    print("Camera not found. Please add a camera and try again.")
    return False


def AcquireMoveAndLock(name):
    print("Acquiring...")

    # Generating the experiment file name
    name += 'PL'.format(experiment.GetValue(CameraSettings.ShutterTimingExposureTime))\
        .format(experiment.GetValue(ExperimentSettings.FileNameGenerationAttachDate))\
        .format(experiment.GetValue(ExperimentSettings.FileNameGenerationAttachTime))
    # You could add spectrometer center wavelength to the name by adding
    # \,experiment.GetValue(SpectrometerSettings.GratingCenterWavelength))
    # To the previous code

    # Setting the basefilename of the experiment to the 'name' we defined below
    experiment.SetValue(ExperimentSettings.FileNameGenerationBaseFileName, name)

    # Performing the experiment, This is asynchronous function, after running acquire system will run the next command

    experiment.Acquire()

    # acquireCompleted is defined as an autoreset event. It is initally set to false before the loop, meaning thread can run
    # Here, we ask program to set the autorest event to true and wait until acquireCompleted event sets it back to false
    # experiment_complete is a call back function and is already hooked(listens) to the experiment_event declration from lightfield
    # Listener will not be locked while the thread is locked (the key thing that makes this happen)
    # When experiment is completed. experiment_complete is triggered by the event argument, causing acquireCompleted to set to false
    # acquirecompleted function is basically experiment_complete set but with a note

    acquireCompleted.WaitOne()


def get_spectrometer_info():
    print(String.Format("{0} {1}", "Center Wave Length:",
                        str(experiment.GetValue(
                            SpectrometerSettings.GratingCenterWavelength))))

    print(String.Format("{0} {1}", "Grating:",
                        str(experiment.GetValue(
                            SpectrometerSettings.Grating))))


def prepare_grating(center_wave):
    if code_type == 1:
        print("Choosing the grating")
        #experiment.SetValue(SpectrometerSettings.GratingSelected, '[750nm,300][0][0]')  #500nm blaze 1200gr gr no 2 (2-1=1) on turret 1 (0)
        print("Setting the center wavelength")
        experiment.SetValue(SpectrometerSettings.GratingCenterWavelength, center_wave)
        # sensor_calibration = experiment.GetValue() Need to work on this later.
        #print("Selected grating is",format(experiment.GetValue(SpectrometerSettings.GratingSelected)))
    else:
        print("experiment running in demo mode, no spectrometer or grating defined")
        return


def get_current_temperature():
    print(String.Format(
        "{0} {1}", "Current Temperature:",
        experiment.GetValue(CameraSettings.SensorTemperatureReading)))
    return int(experiment.GetValue(CameraSettings.SensorTemperatureReading))



def check_camera_temperature():
    if code_type == 1:
        camera_temperature = get_current_temperature()
        while camera_temperature > -69.6:
            print("Camera is at", camera_temperature,"C. Waiting to reach -70C")
            time.sleep(2)
            camera_temperature = get_current_temperature()
    else:
        print("Demo Camera in action, skipping temperature check")


def load_experiment():
    if code_type == 1:
        experiment.Load('PLRED')
        print("real experiment is loading")
    else:
        experiment.Load('Demopixis')
        print("Demo experiment is loading")


# ------------------------------------------------ Main Code -----------------------------------
# The main code section

# First we check to see if MDT693B is connected. If connected, we open lightfield and set the settings
# ----------------------------------------------------- START
device_ip = '192.168.254.254'
device_port = 5001

esp = ESP(device_ip, device_port)
axis_x = esp.axis(1)
axis_y = esp.axis(2)
axis_x.on()
axis_y.on()

# ----------------------------------------------------- END

# Opening lightfield and initialization of settings
# ----------------------------------------------------- START

auto = Automation(True, List[String]())
experiment = auto.LightFieldApplication.Experiment
load_experiment()
# The 2nd parameter forces LF to load with no experiment,  Get experiment object



# Now we check to see if the camera and the spectrometer are connected. If they are we continue.
# I should add the temperature check here as well

check_camera_exist()
check_spectrometer_exist()
check_camera_temperature()
# We configure our PLmap


global acquireCompleted
acquireCompleted = AutoResetEvent(False)

# Loading the experiment

sensor_height = experiment.GetValue(CameraSettings.SensorInformationActiveAreaHeight)
sensor_width = experiment.GetValue(CameraSettings.SensorInformationActiveAreaWidth)
PLmap = np.zeros((int(x_step_range), int(y_step_range), int(sensor_width)))
prepare_grating(center_wavelength)
print("waiting 15 seconds for everything to settle")
time.sleep(15)



print(np.shape(PLmap))
setROI()


# Initilize the filename parameters

InitializeFilenameParams()

# Hooking the listener. This line means the experiment_completed will always be hooked to the event of the Experiment
# It will listen to it through out the code

experiment.ImageDataSetReceived += experiment_completed

# Experiment Settings

# experiment.SetValue(SpectrometerSettings.GratingSelected,'[500nm,1200].[1][0]')    # example code for grating control
# experiment.SetValue(SpectrometerSettings.GratingCenterWavelength, 780)             # sample code for setting center gr
experiment.SetValue(CameraSettings.ShutterTimingExposureTime, t_exp*1000)
experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore, 1)
print("Active sensor width is", sensor_width)
baseFilename = "PLmap_demo_"
# ----------------------------------------------------- END
#

# initialize the communication with the piezo-stage and set it to (0,0)
# initialize the pl_plot
# ----------------------------------------------------- START

print("Moving in voltage steps of", increment, "mm with interval times of", t_exp, "seconds")
axis_x.move_to(originx)
axis_y.move_to(originy)
print("stage initilized to zero position, X and Y are set to zero")
time.sleep(3)
# ----------------------------------------------------- END




# Starting the double piezo loop, within each loop a frame capture event occurs
# Note that we are doing a an intermittent reverse loop. Loop v_y changes direction
# each time it does a loop. We don't want the piezos to do large movement when each row is changed
# x and y are the global variables that denote the pixel location in the final PL picture
# ----------------------------------------------------- START
x = 0
y = 0
v_x = 0
v_y = 0

PL_plot = np.zeros((int(x_step_range),int(y_step_range)))
for v_x in np.arange(0, range, increment):
    x= int(v_x/increment)
    if v_x != 0:
        axis_x.move_by(increment)
    time.sleep(0.3)
    if v_y == 0:
        for v_y in np.arange(0, range, increment):
            y = int(v_y/increment)
            axis_y.move_by(increment)
            time.sleep(0.3)
            print("we are in position ", x, y)
            AcquireMoveAndLock(baseFilename)
            time.sleep(0.8)
            time.sleep(t_exp)
    elif v_y == range - increment:
        for v_y in reversed(np.arange(0, range, increment)):
            y = int(v_y/increment)
            axis_y.move_by(-1 * increment)
            time.sleep(0.3)
            print("we are in position ", x, y)
            AcquireMoveAndLock(baseFilename)
            time.sleep(t_exp)
            time.sleep(0.8)

    else:
        print("an error has occured in movement of stage")
        print("last scanned position was pixel", x,y)
        exit()
print("PL Map completed, application will save and abort")
# ----------------------------------------------------- END

#Plotting and saving data before closing the app
# ----------------------------------------------------- START

ani = FuncAnimation(fig, update_plot, frames=num_frames, blit=True)


# time.sleep(3)
# print(PL_plot)
# plt.imshow(np.flip(PL_plot,0), cmap='Greys', interpolation='nearest')
# plt.title("PL data realtime normalized")
# plt.ion()
# plt.show()
# now = datetime.now()
# save_filename = 'PLmap' + now.strftime("%d-%m-%Y-%H-%M-%S")
# save_data = save_filename + '.npy'
# save_map = save_filename + '.png'

# np.save(save_data, PLmap)
# plt.savefig(save_map)

# ----------------------------------------------------- END
auto.Dispose()
exit()
