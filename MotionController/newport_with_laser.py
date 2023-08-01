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
v_res = 1       # voltage spacing of the piezo
v_range =50  # total voltage movement of the piezo
t_exp = 0.5     # exposure time in seconds
x_step_range = v_range/v_res
y_step_range = v_range/v_res
ROI_y_origin = 98
ROI_y_height = 17

# Function Definitions for the MDT693B
def CommonFunc(serialNumber):
    hdl = mdtOpen(serialNumber, 115200, 3)
    # or check by "mdtIsOpen(devs[0])"
    if (hdl < 0):
        print("Connect ", serialNumber, "fail")
        return -1
    else:
        print("Connect ", serialNumber, "successful")

    result = mdtIsOpen(serialNumber)
    print("mdtIsOpen ", result)

    id = []
    result = mdtGetId(hdl, id)
    if (result < 0):
        print("mdtGetId fail ", result)
    else:
        print(id)

    limitVoltage = [0]
    result = mdtGetLimtVoltage(hdl, limitVoltage)
    if (result < 0):
        print("mdtGetLimtVoltage fail ", result)
    else:
        print("mdtGetLimtVoltage ", limitVoltage)
    return hdl
def Read_X(hdl):
    voltage = [0]
    result = mdtGetXAxisVoltage(hdl,voltage)
    if (result < 0):
        print("X Voltage READ fail ", result)
    else:
        print("X Voltage READ ", voltage)
def Set_X(hdl, vnext):
    result = mdtSetXAxisVoltage(hdl, vnext)
    if (result < 0):
        print("X Voltage fail ", result)
    else:
        print("X Voltage SET ", vnext)
def Read_X_min(hdl):
    minVoltage = [0]
    result = mdtGetXAxisMinVoltage(hdl, minVoltage)
    if (result < 0):
        print("X MinVoltage fail ", result)
    else:
        print("X MinVoltage ", minVoltage)
def Read_X_max(hdl):
    maxVoltage = [0]
    result = mdtGetXAxisMaxVoltage(hdl, maxVoltage)
    if (result < 0):
        print("X MaxVoltage fail ", result)
    else:
        print("X MaxVoltage ", maxVoltage)
def Get_X_step_res(hdl):
    result = mdtGetVoltageAdjustmentResolution(hdl)
    if (result < 0):
        print("mdtGetVoltageAdjustmentResolution fail ", result)
    else:
        print("mdtGetVoltageAdjustmentResolution ", result)
def Read_Y(hdl):
    voltage = [0]
    result = mdtGetYAxisVoltage(hdl,voltage)
    if (result < 0):
        print("Y Voltage READ fail ", result)
    else:
        print("Y Voltage READ ", voltage)
def Set_Y(hdl,vnext):
    result = mdtSetYAxisVoltage(hdl, vnext)
    if (result < 0):
        print("Y Voltage fail ", result)
    else:
        print("Y Voltage SET ", vnext)
def Read_Y_min(hdl):
    minVoltage = [0]
    result = mdtGetYAxisMinVoltage(hdl, minVoltage)
    if (result < 0):
        print("Y MinVoltage fail ", result)
    else:
        print("Y MinVoltage ", minVoltage)
def Read_Y_max(hdl):
    maxVoltage = [0]
    result = mdtGetYAxisMaxVoltage(hdl, maxVoltage)
    if (result < 0):
        print("Y MaxVoltage fail ", result)
    else:
        print("Y MaxVoltage ", maxVoltage)
def Check_X_AXiS(hdl):
    voltage = [0]
    result = mdtGetXAxisVoltage(hdl, voltage)
    if (result < 0):
        print("mdtGetXAxisVoltage fail ", result)
    else:
        print("mdtGetXAxisVoltage ", voltage)

    result = mdtSetXAxisVoltage(hdl, 40)
    if (result < 0):
        print("mdtSetXAxisVoltage fail ", result)
    else:
        print("mdtSetXAxisVoltage ", 40)

    minVoltage = [0]
    result = mdtGetXAxisMinVoltage(hdl, minVoltage)
    if (result < 0):
        print("mdtGetXAxisMinVoltage fail ", result)
    else:
        print("mdtGetXAxisMinVoltage ", minVoltage)

    result = mdtSetXAxisMinVoltage(hdl, 50)
    if (result < 0):
        print("mdtSetXAxisMinVoltage fail ", result)
    else:
        print("mdtSetXAxisMinVoltage ", 50)
    # reset back
    mdtSetXAxisMinVoltage(hdl, minVoltage[0])
    print("mdtSetXAxisMinVoltage ", minVoltage[0])

    maxVoltage = [0]
    result = mdtGetXAxisMaxVoltage(hdl, maxVoltage)
    if (result < 0):
        print("mdtGetXAxisMaxVoltage fail ", result)
    else:
        print("mdtGetXAxisMaxVoltage ", maxVoltage)

    result = mdtSetXAxisMaxVoltage(hdl, 60)
    if (result < 0):
        print("mdtSetXAxisMaxVoltage fail ", result)
    else:
        print("mdtSetXAxisMaxVoltage ", 60)
    # reset back
    mdtSetXAxisMaxVoltage(hdl, maxVoltage[0])
    print("mdtSetXAxisMaxVoltage ", maxVoltage[0])
def Check_Y_AXiS(hdl):
    voltage = [0]
    result = mdtGetYAxisVoltage(hdl, voltage)
    if (result < 0):
        print("mdtGetYAxisVoltage fail ", result)
    else:
        print("mdtGetYAxisVoltage ", voltage)

    result = mdtSetYAxisVoltage(hdl, 40)
    if (result < 0):
        print("mdtSetYAxisVoltage fail ", result)
    else:
        print("mdtSetYAxisVoltage ", 40)

    minVoltage = [0]
    result = mdtGetYAxisMinVoltage(hdl, minVoltage)
    if (result < 0):
        print("mdtGetYAxisMinVoltage fail ", result)
    else:
        print("mdtGetYAxisMinVoltage ", minVoltage)

    result = mdtSetYAxisMinVoltage(hdl, 50)
    if (result < 0):
        print("mdtSetYAxisMinVoltage fail ", result)
    else:
        print("mdtSetYAxisMinVoltage ", 50)
    # reset back
    mdtSetYAxisMinVoltage(hdl, minVoltage[0])
    print("mdtSetYAxisMinVoltage ", minVoltage[0])

    maxVoltage = [0]
    result = mdtGetYAxisMaxVoltage(hdl, maxVoltage)
    if (result < 0):
        print("mdtGetYAxisMaxVoltage fail ", result)
    else:
        print("mdtGetYAxisMaxVoltage ", maxVoltage)

    result = mdtSetYAxisMaxVoltage(hdl, 40)
    if (result < 0):
        print("mdtSetYAxisMaxVoltage fail ", result)
    else:
        print("mdtSetYAxisMaxVoltage ", 40)
    # reset back
    mdtSetYAxisMaxVoltage(hdl, maxVoltage[0])
    print("mdtSetYAxisMaxVoltage ", maxVoltage[0])
def Check_Z_AXiS(hdl):
    voltage = [0]
    result = mdtGetZAxisVoltage(hdl, voltage)
    if (result < 0):
        print("mdtGetZAxisVoltage fail ", result)
    else:
        print("mdtGetZAxisVoltage ", voltage)

    result = mdtSetZAxisVoltage(hdl, 40)
    if (result < 0):
        print("mdtSetZAxisVoltage fail ", result)
    else:
        print("mdtSetZAxisVoltage ", 40)

    minVoltage = [0]
    result = mdtGetZAxisMinVoltage(hdl, minVoltage)
    if (result < 0):
        print("mdtGetZAxisMinVoltage fail ", result)
    else:
        print("mdtGetZAxisMinVoltage ", minVoltage)

    result = mdtSetZAxisMinVoltage(hdl, 50)
    if (result < 0):
        print("mdtSetZAxisMinVoltage fail ", result)
    else:
        print("mdtSetZAxisMinVoltage ", 50)
    # reset back
    mdtSetZAxisMinVoltage(hdl, minVoltage[0])
    print("mdtSetZAxisMinVoltage ", minVoltage[0])

    maxVoltage = [0]
    result = mdtGetZAxisMaxVoltage(hdl, maxVoltage)
    if (result < 0):
        print("mdtGetZAxisMaxVoltage fail ", result)
    else:
        print("mdtGetZAxisMaxVoltage ", maxVoltage)

    result = mdtSetZAxisMaxVoltage(hdl, 60)
    if (result < 0):
        print("mdtSetZAxisMaxVoltage fail ", result)
    else:
        print("mdtSetZAxisMaxVoltage ", 60)
    # reset back
    mdtSetZAxisMaxVoltage(hdl, maxVoltage[0])
    print("mdtSetZAxisMaxVoltage ", maxVoltage[0])
def MDT693BExample(serialNumber):
    hdl = CommonFunc(serialNumber)
    if (hdl < 0):
        return
    Check_X_AXiS(hdl)
    Check_Y_AXiS(hdl)
    Check_Z_AXiS(hdl)

    result = mdtSetMasterScanEnable(hdl, 0)
    if (result < 0):
        print("mdtSetMasterScanEnable fail ", result)
    else:
        print("mdtSetMasterScanEnable ", 0)

    result = mdtSetAllVoltage(hdl, 5)
    if (result < 0):
        print("mdtSetAllVoltage fail ", result)
    else:
        print("mdtSetAllVoltage ", 5)

    xVoltage = 10
    yVoltage = 20
    zVoltage = 30
    result = mdtSetXYZAxisVoltage(hdl, xVoltage, yVoltage, zVoltage)
    if (result < 0):
        print("mdtSetXYZAxisVoltage fail ", result)
    else:
        print("mdtSetXYZAxisVoltage ", xVoltage, yVoltage, zVoltage)

    xyzVoltage = [0, 0, 0]
    result = mdtGetXYZAxisVoltage(hdl, xyzVoltage)
    if (result < 0):
        print("mdtGetXYZAxisVoltage fail ", result)
    else:
        print("mdtGetXYZAxisVoltage ", xyzVoltage)

    state = [0]
    result = mdtGetMasterScanEnable(hdl, state)
    if (result < 0):
        print("mdtGetMasterScanEnable fail ", result)
    else:
        print("mdtGetMasterScanEnable ", state)

    result = mdtSetMasterScanEnable(hdl, 1)
    if (result < 0):
        print("mdtSetMasterScanEnable fail ", result)
    else:
        print("mdtSetMasterScanEnable ", 1)

    result = mdtSetMasterScanVoltage(hdl, 5)
    if (result < 0):
        print("mdtSetMasterScanVoltage fail ", result)
    else:
        print("mdtSetMasterScanVoltage ", 5)

    masterVoltage = [0]
    result = mdtGetMasterScanVoltage(hdl, masterVoltage)
    if (result < 0):
        print("mdtGetMasterScanVoltage fail ", result)
    else:
        print("mdtGetMasterScanVoltage ", masterVoltage)
    result = mdtClose(hdl)
    if (result == 0):
        print("mdtClose ", serialNumber)
    else:
        print("mdtClose fail", result)
    result = mdtIsOpen(serialNumber)
    print("mdtIsOpen ", result)
def check_hdl():
    if (hdl < 0):
     return
# Function Definitions for the CCD and the Spectrometer
def Max_int_PLmap(incoming_data):
    incoming_data = np.max(incoming_data)
    print("c1")
    PL_plot[x][y] = incoming_data
    print("c2")
    print(PL_plot)
    plt.imshow(np.flip(PL_plot,0), cmap='Greys', interpolation='nearest')
    plt.title("PL data realtime normalized")
    plt.ion()
    plt.draw()
    plt.pause(1)
    print("c3")
    plt.close()

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
try:
    devs = mdtListDevices()
    print(devs)
    if (len(devs) <= 0):
        print('There is no devices connected')
        exit()

    for mdt in devs:
        if (mdt[1] == "MDT693B"):
            print('MDT693B Device is recognized')
            print('Establishing Connection Now...')
            hdl = CommonFunc(mdt[0])    #It appears we would like to pass mdt[0] instead of the serial number
            check_hdl()
        elif (mdt[1] == "MDT694B"):
            print('we dont recognize this device')
except Exception as ex:
    print("Warning:", ex)
    print("*** End ***")
    input()
print("success in breaking")
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

print("Moving in voltage steps of", v_res, "volt with interval times of", t_exp, "seconds")
Set_X(hdl, 0)
Set_Y(hdl, 0)
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
v_x=0
v_y=0
PL_plot = np.zeros((int(x_step_range),int(y_step_range)))
for v_x in np.arange(0, v_range, v_res):
    x= int(v_x/v_res)
    Set_X(hdl, v_x)
    time.sleep(0.3)
    Read_X(hdl)
    Read_Y(hdl)
    if v_y == 0:
        for v_y in np.arange(0, v_range, v_res):
            y = int(v_y/v_res)
            Set_Y(hdl, v_y)
            time.sleep(0.3)
            Read_X(hdl)
            Read_Y(hdl)
            print("we are in position ", x, y)
            AcquireMoveAndLock(baseFilename)
            time.sleep(0.8)
            time.sleep(t_exp)
    elif v_y == v_range - v_res:
        for v_y in reversed(np.arange(0, v_range, v_res)):
            y = int(v_y/v_res)
            Set_Y(hdl, v_y)
            time.sleep(0.3)
            Read_X(hdl)
            Read_Y(hdl)
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

time.sleep(3)
print(PL_plot)
plt.imshow(np.flip(PL_plot,0), cmap='Greys', interpolation='nearest')
plt.title("PL data realtime normalized")
plt.ion()
plt.show()
now = datetime.now()
save_filename = 'PLmap' + now.strftime("%d-%m-%Y-%H-%M-%S")
save_data = save_filename + '.npy'
save_map = save_filename + '.png'

np.save(save_data, PLmap)
plt.savefig(save_map)

# ----------------------------------------------------- END
auto.Dispose()
exit()
