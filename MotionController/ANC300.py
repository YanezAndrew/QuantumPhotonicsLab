from pymeasure.instruments.attocube.anc300 import ANC300Controller
from pymeasure.instruments.attocube.anc300 import Axis
import numpy as np
import pandas as pd
from time import sleep

# Set the input parameters
data_points = 50
averages = 10
max_current = 0.001
min_current = -max_current

# Set source_current and measure_voltage parameters
current_range = 10e-3  # in Amps
compliance_voltage = 10  # in Volts
measure_nplc = 0.1  # Number of power line cycles
voltage_range = 1  # in VOlts
#(adapter = TCPIP::<address>::<port>::SOCKET”, axisnames, passwd)
ANC300Controller()