# Imports and Declarations

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
import matplotlib as plt
import ctypes
import time

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
# from PrincetonInstruments.LightField.AddIns import SpectrometerSettings


# Global parameter declaration (experiment properties)

serialNumber = 2108112774

v_res = 2       # voltage spacing of the piezo
v_range = 10    # total voltage movement of the piezo
t_exp = 1       # exposure time
x_step_range= v_range/v_res
y_step_range= v_range/v_res
ROI_y_origin= 30
ROI_y_height= 15
sensor_width = 100  #will update this to the full sensor width later

# Function Definitions for the MDT693B

def CommonFunc(serialNumber):
    hdl = mdtOpen(serialNumber, 115200, 3)
    # or check by "mdtIsOpen(devs[0])"
    if (hdl < 0):
        print("Connect ", serialNumber, "fail")
        return-1
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

# Function Definitions for the CCD and the Spectrometer
def check_camera_exist():
    if (device_found() == True):
        return
    else:
        print("camera not found")
        exit()

def PLmapcapture(new_data):
    PLmap[1][1] = new_data
    print(PLmap)

def device_found():
    # Find connected device
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
    im = np.reshape(im,(1, 100))  # this one and hundred are the size of my ROI
    print("t7")
    return im

def setROI():
    #sensorCols = experiment.GetValue(CameraSettings.SensorInformationActiveAreaWidth)
    #sensorRows = experiment.GetValue(CameraSettings.SensorInformationActiveAreaHeight)
    experiment.SetCustomRegions([RegionOfInterest(1, ROI_y_origin, sensor_width, ROI_y_height, 1, ROI_y_height)])
    #RegionofInterest(x_origin,y_origin,x_width,y_height,x_binning,y_binning)

def InitializeFilenameParams():
    experiment.SetValue(ExperimentSettings.FileNameGenerationAttachIncrement, True)
    experiment.SetValue(ExperimentSettings.FileNameGenerationIncrementNumber,1)
    experiment.SetValue(ExperimentSettings.FileNameGenerationIncrementMinimumDigits, 2)
    experiment.SetValue(ExperimentSettings.FileNameGenerationAttachDate,False)
    experiment.SetValue(ExperimentSettings.FileNameGenerationAttachTime, False)

def experiment_completed(sender, event_args):
    print("...Acquisition Complete!)")
    #global i
    frames = event_args.ImageDataSet.Frames
    print("t1")
    #i+=frames
    buffer = event_args.ImageDataSet.GetFrame(0, frames-1) #1st ROI and most recent frame in the event
    image_data = buffer.GetData()
    data_array = ManipulateImageData(image_data, buffer)
    print(data_array)
    print(type(data_array))
    PLmapcapture(data_array)
    return np.copy(data_array)
    acquireCompleted.Set()

def device_found():
    # Find connected device
    for device in experiment.ExperimentDevices:
        if (device.Type == DeviceType.Camera):
            return True

    # If connected device is not a camera inform the user
    print("Camera not found. Please add a camera and try again.")
    return False

def AcquireMoveAndLock(name):
    print("Acquiring...")

    # Generating the experiment file name
    name += 'testrun1_'.format(experiment.GetValue(CameraSettings.ShutterTimingExposureTime))
    # You could add spectrometer center wavelength to the name by adding
    # \,experiment.GetValue(SpectrometerSettings.GratingCenterWavelength))
    # To the previous code

    setROI()


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

def do_my_experiment():
    # Event alert
    global acquireCompleted
    acquireCompleted = AutoResetEvent(False)

    # Loading the experiment
    experiment.Load('Demopixis')

    # Initilize the filename parameters

    InitializeFilenameParams()

    # Hooking the listener. This line means the experiment_completed will always be hooked to the event of the Experiment
    # It will listen to it through out the code

    experiment.ImageDataSetReceived += experiment_completed

    # Experiment Settings

    # experiment.SetValue(SpectrometerSettings.GratingSelected,'[500nm,1200].[1][0]')    # example code for grating control
    # experiment.SetValue(SpectrometerSettings.GratingCenterWavelength, 780)             # sample code for setting center gr
    experiment.SetValue(CameraSettings.ShutterTimingExposureTime, 100)
    experiment.SetValue(ExperimentSettings.AcquisitionFramesToStore, 1)
    width = experiment.GetValue(CameraSettings.SensorInformationActiveAreaWidth)
    height = experiment.GetValue(CameraSettings.SensorInformationActiveAreaHeight)

    baseFilename = "PLmap_demo_"

    AcquireMoveAndLock(baseFilename)


# The main code section

# First we check to see if MDT693B is connected. If connected, we open lightfield
# ----------------------------------------------------- START
try:
    devs = mdtListDevices()
    print(devs)
    if (len(devs) <= 0):
        print('There is no devices connected')
        exit()

    for mdt in devs:
        if (mdt[1] == "MDT693B"):
            print('MDT693B Device is recognized and conneccted')
            print('running subsequent program')
            break
        elif (mdt[1] == "MDT694B"):
            print('we dont recognize this device')
except Exception as ex:
    print("Warning:", ex)
    print("*** End ***")
    input()
print("sucess in breaking")
# ----------------------------------------------------- END

# Opening lightfield and initalizalization of settings
# ----------------------------------------------------- START
auto = Automation(True, List[String]())

# The 2nd parameter forces LF to load with no experiment,  Get experiment object
experiment = auto.LightFieldApplication.Experiment

# We configure our PLmap
PLmap = np.zeros((x_step_range, y_step_range, sensor_width))

# Now we check to see if the camera is connected. If it is we continue.
# I should add the temperature check here as well
check_camera_exist()
# ----------------------------------------------------- END
#

# initialize the communication with the piezo-stage and set it to (0,0)
# ----------------------------------------------------- START
hdl = CommonFunc(serialNumber)
# if (hdl < 0):
#     return
print("Moving in voltage steps of", v_res, "volt with interval times of", t_exp, "seconds")
Set_X(hdl, 0)
Set_Y(hdl, 0)
print("stage initilized to zero position, X and Y are set to zero")
time.sleep(3)
# ----------------------------------------------------- END

# Starting the double piezo loop, within each loop a frame capture event occurs

for v_x in np.arange(0, v_range, v_res):
    Set_X(hdl, v_x)
    time.sleep(t_exp)
    Read_X(hdl)
    Read_Y(hdl)
    time.sleep(0.2)
    for v_y in np.arange(0, v_range, v_res):
        Set_Y(hdl, v_y)
        time.sleep(t_exp)
        Read_X(hdl)
        Read_Y(hdl)
        time.sleep(0.2)



do_my_experiment()
auto.Dispose()

xscan(mdt[0])