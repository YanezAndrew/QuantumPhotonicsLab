import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import datetime

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
    for timestamp, value in read_data('data.csv'):
        xs.append(timestamp)
        ys.append(value)
    
    ax.clear()
    ax.plot(xs, ys, '-o')
    ax.set_xlabel('Time')
    ax.set_ylabel('Temp (K)')
    date_str = datetime.datetime.now().strftime('%B %d')
    ax.text(0.95, 0.95, date_str, transform=ax.transAxes,
             horizontalalignment='right', verticalalignment='top', fontsize=12)
    
    # Limit the number of x-values shown per time
    tick_frequency = 1  # Show a tick every 5 data points
    ax.set_xticks(ax.get_xticks()[::tick_frequency])
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)

if __name__ == "__main__":
    #style.use('fivethirtyeight')

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    
    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
