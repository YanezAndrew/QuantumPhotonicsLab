import pandas as pd
import matplotlib.pyplot as plt
import ast
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import ListedColormap
import time
from decimal import Decimal
start_time = time.time()
# 'data_2023-08-10 (50) - Lucidean.csv'
# 'data_2023-08-18 (5) - Lucidean_2.csv'
# 'data_2023-08-22 (4) - Lucidean_2nDevice.csv'

df = pd.read_csv('data_2023-08-22 (4) - Lucidean_2nDevice.csv')
df = df.sort_values(by='Temperature', ascending=False)
df.reset_index(drop=True, inplace=True)
df['Voltage'] = df['Voltage'].apply(ast.literal_eval)
df['Amps'] = df['Amps'].apply(ast.literal_eval)

xvals = np.array(df['Voltage'].values[0])
fig, ax = plt.subplots(figsize=(16, 9))
fig.suptitle("Lucidean EOM Temperature IV - Device #2")

cm = plt.cm.get_cmap("jet").reversed()
# num_colors = len(df['Temperature'])  # Adjust the number of colors as needed
# color_array = plt.cm.jet(np.linspace(0, 1, num_colors))
# cm = LinearSegmentedColormap.from_list('custom_jet', color_array, N=num_colors)
# cm = cm.reversed()
#norm = plt.Normalize(vmin=min(df['Temperature']), vmax=max(df['Temperature']))
#print(cm(norm(range(len(df['Temperature'])))))

plt.xlim(0, 1.5)
plt.ylim(1e-14, 5e-3)

prev = df['Temperature'][0]
num_curves = len(df['Temperature'])
add = 0.0
max_temp = max(df['Temperature'])
min_temp = min(df['Temperature'])
range = round(max_temp-min_temp, 3)

unique_ordered_elements = []
unique_ordered_temp = []
test_cnt = 0
for cnt, i in enumerate(df['Temperature']):
    if cnt == 0:
        prev_color = cm(0.0)
        dx = 0.0
        plt.semilogy(xvals, np.abs(df['Amps'][0]), color=cm(dx), label=f'Curve {i + 1}')
    else:
        dx = round(prev - i, 3)
        prev = i
        add = round(add + dx, 3)
        color = cm(add / range)
        if dx > 0.0:
            unique_ordered_temp.append(i)
            unique_ordered_elements.append(color)
            plt.semilogy(xvals, np.abs(df['Amps'][cnt]), color=color, label=f'Curve {i + 1}')
            #test_cnt +=1
            prev_color = color
        #plt.pause(0.000001)
# Add a color bar
#print(test_cnt)
#cmap = ListedColormap(unique_ordered_elements).reversed()
normalize = plt.Normalize(max_temp, min_temp)
sm = plt.cm.ScalarMappable(cmap=cm.reversed(), norm = normalize)
#print("Last Temp Before Color Doesn't Change Anymore:", min(unique_ordered_temp))

# # Choose a subset of temperature ticks to display on the color bar
num_ticks = 5  # Number of ticks to display
tick_indices = np.linspace(0, len(unique_ordered_temp) - 1, num_ticks, dtype=int)
cbar_ticks = [unique_ordered_temp[i] for i in tick_indices]
cbar_ticks = [max_temp, 215.3, 125, min_temp]
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
