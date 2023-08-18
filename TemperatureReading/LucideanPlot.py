import pandas as pd
import matplotlib.pyplot as plt
import ast
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

df = pd.read_csv('data_2023-08-10 (50) - Lucidean.csv')
df['Voltage'] = df['Voltage'].apply(ast.literal_eval)
df['Amps'] = df['Amps'].apply(ast.literal_eval)
xvals = np.array(df['Voltage'].values[0])
plt.figure(dpi=150)

# Create a custom colormap with increased intensity for negative slopes
#colors = [(1, 1, 0), (0, 0, 1)]  # Yellow to Blue
#cmap_name = 'yellow_to_blue'
cm = plt.cm.get_cmap("jet").reversed()
plt.xlim(0, 1.5)
plt.ylim(1e-14, 10e-3)
prev = df['Temperature'][0]
num_curves = len(df['Temperature'])
add = 0.000
max_temp = df['Temperature'][0]
for cnt, i in enumerate(df['Temperature']):
    if cnt == 0:
        dx = 0
    else:
        dx = prev - i
        prev = i
        add += dx
        color = cm(add / max_temp)
        #print(color)
        plt.semilogy(xvals, np.abs(df['Amps'][cnt]), color=color, label=f'Curve {i + 1}')
        #plt.legend()
        #plt.pause(0.000001)
plt.xlabel("Voltage [V]")
plt.ylabel("Amps [Log(A)]")
plt.show()
