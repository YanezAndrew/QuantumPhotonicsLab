import pyvisa as pv
import time
import sys
import numpy as np
import matplotlib.pyplot as plt

rm = pv.ResourceManager()
print(rm.list_resources())
keysight = rm.open_resource(rm.list_resources()[0])
print(keysight.query('*IDN?'))
print(rm)
print(keysight)
keysight.write('*RST')
time.sleep(0.1)

keysight.write(":SOUR:FUNC:MODE VOLT")
keysight.write(":SOUR:VOLT 1")
keysight.write(":OUTP ON")
time.sleep(5)
#keysight.write(":MEAS:RES? (@1)")
#data = keysight.read()
keysight.write(":MEAS:CURR? (@1)")
curr = keysight.read()
#print(data)
print(curr)
time.sleep(0.1)
keysight.write(":OUTP OFF")