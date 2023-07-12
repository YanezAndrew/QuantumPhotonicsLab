import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
from datetime import datetime
import os

def read_data(filename):
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                try:
                    timestamp, value = line.split(',')
                    yield timestamp[10:19], float(value)
                except (ValueError, IndexError):
                    continue

def animate(i):
    xs = []
    ys = []
    for timestamp, value in read_data(file_path):
        xs.append(timestamp)
        ys.append(value)
    
    ax.clear()
    ax.plot(xs, ys, '-o')
    ax.set_xlabel('Time')
    ax.set_ylabel('Temp (K)')
    date_str = datetime.now().strftime('%B %d')
    ax.text(0.95, 0.95, date_str, transform=ax.transAxes,
             horizontalalignment='right', verticalalignment='top', fontsize=12)
    
    # Limit the number of x-values shown per time
    tick_frequency = 1  # Show a tick every 5 data points
    ax.set_xticks(ax.get_xticks()[::tick_frequency])
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)

if __name__ == "__main__":
    #style.use('fivethirtyeight')
    current_dir = os.getcwd()
    
    # Get the current date
    current_date = datetime.now().strftime('%Y-%m-%d')
    cnt = 0
    # File name with the current date
    file_name = f"data_{current_date} ({cnt}).csv"

    # Path to the file in the current directory
    file_path = os.path.join(current_dir, file_name)

    # Check if the file already exists
    file_exists = os.path.exists(file_path)
    
    # If the file already exists, add a number to the file name
    while (file_exists == False):
        file_name = f"data_{current_date} ({cnt}).csv"
        file_path = os.path.join(current_dir, file_name)
        file_exists = os.path.exists(file_path)
        cnt += 1

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
