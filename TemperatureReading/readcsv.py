import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import datetime

def animate(i):
    graph_data = open('data.csv', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    for line in lines:
        if len(line) > 1:
            x, y = line.split(',')
            try:
                xs.append(x[10:19])
                ys.append(float(y))
            except ValueError:
                continue
    
    ax1.clear()
    # Set the figure size
    ax1.plot(xs, ys, '-o')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Temp (K)')
    date_str = datetime.datetime.now().strftime('%B %d')
    ax1.text(0.95, 0.95, date_str, transform=ax1.transAxes,
             horizontalalignment='right', verticalalignment='top', fontsize=12)



if __name__ == "__main__":
    #style.use('fivethirtyeight')

    fig = plt.figure()
    ax1 = fig.add_subplot(1, 1, 1)
    

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show()
