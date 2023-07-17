import pyvisa as pv
import time
import numpy as np
import matplotlib.pyplot as plt


def single_IV_sweep(keysight=None, channel=1, start=0, stop=10, points=10, aper=1E-4, current_compliance=0.1):
    '''
        Remember to connect, initialze keysight and import numpy before executing this function!
        Runs an IV measurement on Channel 1.
        Return a numpy array with the current values.
    '''

    # Source
    keysight.write("*RST")
    #keysight.write(":SOUR:FUNC:MODE VOLT")
    keysight.write(":SOUR:VOLT:MODE SWE")
    #keysight.write(":SOUR:VOLT:RANG:AUTO:LLIM 0.002")
    keysight.write(":SOUR:VOLT:STAR " + str(start))
    keysight.write(":SOUR:VOLT:STOP " + str(stop))
    keysight.write(":SOUR:VOLT:POIN " + str(points))

    # Sense
    keysight.write(":SENSE:FUNC ""CURR""")
    #keysight.write(":SENSE:CURR:RANG:AUTO OFF")
    #keysight.write(":SENSE:CURR:RANG 1E-9")
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

# keysight.read_termination = '\n'
# keysight.write_termination = '\n'

'''
    code for testing if keysight is connected successfully
'''
print(keysight)
print(keysight.query('*IDN?')) # return ID information
keysight.write('*RST') # to reset all setup on the keysight
time.sleep(0.1)



# initializing the parameters
start = 0
stop = 1
points = 75
save_file = False

volt_list = np.linspace(start, stop, points)
M = np.zeros((10, points))
for i in range(10):
    M[i] = single_IV_sweep(keysight, 1, start, stop, points, aper=0.005, current_compliance=2e-4)


# data = single_IV_sweep(keysight,1, start,stop,points, nplc=0.2, current_compliance=10e-9)
# m = np.zeros((2, points), dtype=np.float64) # m is the matrix where the first row is the voltage, and the second row is corresponding current
# m[0] = np.linspace(start, stop, points)
# m[1] = data
# print("The voltages and corresponding currents are: ",m)
# para = np.polyfit(m[0], m[1], 1)




# saving the file
if save_file:
    filename = "4-28-Guang-LED.csv"
    np.savetxt(filename, m, delimiter=',')

keysight.close()

plt.scatter(np.linspace(start, stop, points), np.mean(M, axis=0), s=6)
plt.title("Diode IV")
plt.show()
# print(np.mean(M, axis=0))
# print(np.mean(M, axis=0).shape)
# plt.scatter(np.linspace(start, stop, points), data - np.linspace(start, stop,points) * para[0] - para[1])
# plt.show()
#
# print("Noise level: ", np.std(data - np.linspace(start, stop,points) * para[0] - para[1]))