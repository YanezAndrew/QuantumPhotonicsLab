import pandas as pd
import matplotlib.pyplot as plt
import ast
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap
import time
start_time = time.time()
# 'data_2023-08-10 (50) - Lucidean.csv'
df = pd.read_csv('data_2023-08-18 (5) - Lucidean_2.csv')
df['Voltage'] = df['Voltage'].apply(ast.literal_eval)
df['Amps'] = df['Amps'].apply(ast.literal_eval)
xvals = np.array(df['Voltage'].values[0])
fig, ax = plt.subplots(figsize=(16, 9))
fig.suptitle("Lucidean EOM Temperature IV")

# Create a custom colormap with increased intensity for negative slopes
#colors = [(1, 1, 0), (0, 0, 1)]  # Yellow to Blue
#cmap_name = 'yellow_to_blue'
cm = plt.cm.get_cmap("jet").reversed()
plt.xlim(0, 1.5)
plt.ylim(1e-14, 5e-3)
prev = df['Temperature'][0]
num_curves = len(df['Temperature'])
add = 0.000
max_temp = df['Temperature'][0]
min_temp = min(df['Temperature'])

#print(min_temp)
#cbar_ax = plt.subplot(1, 2, 2)
unique_ordered_elements = []
unique_ordered_temp = []

for cnt, i in enumerate(df['Temperature']):
    if cnt == 0:
        dx = 0
        plt.semilogy(xvals, np.abs(df['Amps'][0]), color=cm(0), label=f'Curve {i + 1}')
    else:
        dx = prev - i
        prev = i
        add += dx
        color = cm(add / (max_temp-min_temp))
        #rint(add/max_temp)
        #print("ADD: ", add)
        if color not in unique_ordered_elements:
            unique_ordered_elements.append(color)
            unique_ordered_temp.append(i)
        #print(color)
        plt.semilogy(xvals, np.abs(df['Amps'][cnt]), color=color, label=f'Curve {i + 1}')
        #plt.pause(0.000001)

# Add a color bar
cmap = ListedColormap(unique_ordered_elements).reversed()
normalize = plt.Normalize(min(unique_ordered_temp), max(unique_ordered_temp))
sm = plt.cm.ScalarMappable(cmap=cmap, norm = normalize)
print(min(unique_ordered_temp))

# # Choose a subset of temperature ticks to display on the color bar
num_ticks = 5  # Number of ticks to display
tick_indices = np.linspace(0, len(unique_ordered_temp) - 1, num_ticks, dtype=int)

cbar_ticks = [unique_ordered_temp[i] for i in tick_indices]

# Create a color bar with custom temperature ticks
cbar = plt.colorbar(sm, ticks=cbar_ticks, ax=ax)
cbar.set_label('Temperature [K]')


end_time = time.time()
runtime = end_time - start_time
print(f"Runtime: {runtime:.6f} seconds")
plt.tight_layout()
plt.xlabel("Voltage [V]")
plt.ylabel("Amps [Log(A)]")
plt.show()
