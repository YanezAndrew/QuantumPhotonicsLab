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






keysight_usb_id = 'USB0::0x0957::0x8C18::MY51145486::INSTR'

rm = pv.ResourceManager()
print(rm)
print(rm.list_resources())
try:
    keysight = rm.open_resource(keysight_usb_id) # open Keysight according to the usb id of keysight that comes along with it.
except:
    print("Failed to connect to Keysight. Please check your connection")
    exit(1)


'''
    code for testing if keysight is connected successfully
'''
print(keysight)
print(keysight.query('*IDN?')) # return ID information
keysight.write('*RST') # to reset all setup on the keysight
time.sleep(0.1)



# initializing the parameters
start = -8
stop = 1
points = 5
save_file = False

M = np.zeros((10, points))
for i in range(10):
    M[i] = single_IV_sweep(keysight, 1, start, stop, points, aper=0.005, current_compliance=2e-4) #2e-4 for a 56k Ohm Resistor


# saving the file
if save_file:
    filename = "4-28-Guang-LED.csv"
    np.savetxt(filename, m, delimiter=',')

keysight.close()


'''
    code for plotting the graph
'''

x = list(np.linspace(start, stop, points))
y = list(np.mean(M, axis=0))

params, covariance = curve_fit(func, x, y)
m_fit, c_fit = params
slope = m_fit
print("Slope: ", slope)

x_fit = np.linspace(min(x), max(x), 100)
y_fit = func(x_fit, m_fit, c_fit)
plt.scatter(x, y, s=6)
slope_text = f"Slope: {slope}"

plt.plot(x_fit, y_fit, linestyle='--', color='red', label=f'Fitted Line ({slope_text})')

print("volts",x)
print("amps",y)

plt.title("Diode IV")
plt.xlabel('Voltage(V)')
plt.ylabel('Current(Amps?)')
plt.legend()
plt.show()