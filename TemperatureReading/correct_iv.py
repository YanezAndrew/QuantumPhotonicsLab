import pyvisa as pv
import time
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def func(x, m, c):
    return m * x + c

def single_IV_sweep(keysight=None, channel=1, start=0, stop=10, points=10, aper=1E-4, current_compliance=0.1):
    '''
        Remember to connect, initialze keysight and import numpy before executing this function!
        Runs an IV measurement on Channel 1.
        Return a numpy array with the current values.
    '''

    # Source
    keysight.write("*RST")
    keysight.write(":SOUR:FUNC:MODE VOLT")
    keysight.write(":SOUR:VOLT:MODE SWE")
    keysight.write(":SOUR:VOLT:STAR " + str(start))
    keysight.write(":SOUR:VOLT:STOP " + str(stop))
    keysight.write(":SOUR:VOLT:POIN " + str(points))

    # Sense
    keysight.write(":SENSE:FUNC ""CURR""")
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
    '''
    #ioObj.WriteString(":#SOUR:VOLT:MODE LIST")
    #ioObj.WriteString(":SOUR:LIST:VOLT 0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1")

    keysight.write(":DISP:ENAB ON")
    keysight.write(":DISP:VIEW GRAP")
    keysight.write(":HCOP:SDUM:FORM JPG")
    keysight.write("*OPC?") 
    keysight.write(":HCOP:SDUM:DATA?")
    '''
    keysight.write(":OUTP" + str(channel) + " OFF")


    # data convertion
    l = data.split(',')
    current_list = np.zeros(points, dtype=np.float64)
    for i in range(points):
        current_list[i] = float(l[i])

    return current_list

def sweeper(volt_start, volt_stop, steps, channel):
    data = []
    keysight.write(":OUTP" + str(channel) + " ON")
    for i, cnt in enumerate(np.linspace(volt_start, volt_stop, steps)):
        #keysight.flush(pv.constants.VI_READ_BUF)
        #keysight.flush(pv.constants.VI_WRITE_BUF_DISCARD)
        #print(cnt)
        keysight.write(":SOUR:VOLT" + str(i))
        keysight.write(":INIT (@" + str(channel) + ")")
        keysight.write(":FETC:CURR? (@" + str(channel) + ")")
        data.append(keysight.read())
        keysight.clear()
    keysight.write(":OUTP" + str(channel) + " OFF")
    return data


####


rm = pv.ResourceManager('@py')
keysight_USB_ID= rm.list_resources()[0]
print(keysight_USB_ID)
#keysight_USB_ID = "USB0::2391::35864::MY51145486::0::INSTR"
try:
    keysight = rm.open_resource(keysight_USB_ID) # open Keysight according to the usb id of keysight that comes along with it.
except:
    print("Failed to connect to Keysight. Please check your connection")
    exit(1)
'''
code for testing if keysight is connected successfully
'''
keysight.write("*RST")
pv.log_to_screen()
keysight.timeout = 5000
keysight.write_termination = "\n"
keysight.read_termination  = "\n"
current_compliance = 5e-2
#keysight.write(":SYST:ERR:ALL?")
#buffer_size = 50000
#keysight.set_visa_attribute(pv.constants.VI_ATTR_RD_BUF_OPER_MODE, buffer_size)
#print(keysight.query('*IDN?')) # return ID information
keysight.write(":SOUR:FUNC:MODE VOLT")
keysight.write(":SENSE:FUNC ""CURR""")
keysight.write(":SENSE:CURR:PROT " + str(0))

# initializing the parameters
save_file = False
start = 0
stop = 1
points = 300

ch = 1
print(sweeper(start, stop, points, ch))
keysight.close()
rm.close()


######




# M = np.zeros((10, points))
# for i in range(10):
#     M[i] = single_IV_sweep(keysight, 1, start, stop, points, aper=0.005, current_compliance=2e-4) #2e-4 for a 56k Ohm Resistor


# # saving the file
# if save_file:
#     filename = "4-28-Guang-LED.csv"
#     np.savetxt(filename, m, delimiter=',')

# keysight.close()


# '''
#     code for plotting the graph
# '''

# x = list(np.linspace(start, stop, points))
# y = list(np.mean(M, axis=0))

# params, covariance = curve_fit(func, x, y)
# m_fit, c_fit = params
# slope = m_fit
# print("Slope: ", slope)

# x_fit = np.linspace(min(x), max(x), 100)
# y_fit = func(x_fit, m_fit, c_fit)
# plt.scatter(x, y, s=6)
# slope_text = f"Slope: {slope}"

# plt.plot(x_fit, y_fit, linestyle='--', color='red', label=f'Fitted Line ({slope_text})')

# print("volts",x)
# print("amps",y)

# plt.title("Diode IV")
# plt.xlabel('Voltage(V)')
# plt.ylabel('Current(Amps?)')
# plt.legend()
# plt.show()