import pandas as pd
import matplotlib.pyplot as plt
import ast
import numpy as np
from matplotlib.colors import LogNorm 
from matplotlib.colors import LinearSegmentedColormap


df = pd.read_csv('data_2023-08-10 (50) - Lucidean.csv')
df['Voltage'] = df['Voltage'].apply(ast.literal_eval)
df['Amps'] = df['Amps'].apply(ast.literal_eval)
xvals = np.array(df['Voltage'].values[0])



plt.figure(dpi=150)

colors = [(1, 1, 0), (0, 0, 0.5)]  # Yellow to Dark Blue
cmap_name = 'yellow_to_dark_blue'
cm = LinearSegmentedColormap.from_list(cmap_name, colors)
num_curves = len(df['Amps'])

for i, current_data in enumerate(df['Amps']):
    color = cm(i / (num_curves - 1)) # Determine color based on the position of the curve
    for value in current_data:
        if abs(value) < 1e-17:
            print(f"Curve {i} has a value less than 1e-17: {value}")
            print(df['Time'][i])
    plt.semilogy(xvals, np.abs(current_data), color=color, label=f'Curve {i + 1}')
#plt.xlim(0, 1.5)
#plt.ylim(1e-14, 10e-3)
plt.xlabel('Voltage [V]')
plt.ylabel('Current [Log(A)]')
plt.show()