import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os
import pandas as pd
import ast

def update(frame):
    # Get the data for the current frame
    x_data = df['Temperature'].iloc[:frame] 
    y_data = df['Resistance'].iloc[:frame]

    # Update the line data
    line.set_data(x_data, y_data)

    # Set plot title and labels (optional)
    ax.set_title('Live Temperature Plot')
    ax.set_xlabel('Temperature')
    ax.set_ylabel('Resistance')


    return line

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
    while (file_exists):
        file_name = f"data_{current_date} ({cnt}).csv"
        file_path = os.path.join(current_dir, file_name)
        file_exists = os.path.exists(file_path)
        cnt += 1
    file_name = f"data_{current_date} ({cnt - 2}).csv"
    if (cnt == -2):
        print("No File Created For Today")
    
    file_path = os.path.join(current_dir, file_name)
    print(file_path)
    df = pd.read_csv(file_path)
    print(df)

    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2)
    
    ani = animation.FuncAnimation(fig, update, frames=len(df), interval=1000)
    plt.show()
