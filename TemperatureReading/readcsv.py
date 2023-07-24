import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import os
import pandas as pd

# def read_data(filename):
#     value_in_desired_row = df.loc[desired_row_index, Temperature]
#     df = pd.read_csv('data.csv', index_col=0)

def read_new_data():
    # Replace this with code to read new data from the data source
    # For example, you can use pd.read_csv(), API calls, or any other method to fetch new data
    new_data = pd.read_csv(file_path)
    return new_data

def animate(frame):
    global df
    new_data = read_new_data()

    # Check if new data is available and update the DataFrame
    if not new_data.empty and not new_data.equals(df):
        df = new_data

    # Here, you can plot/animate the data in 'df'
    # For example, if you have 'temperature' and 'resistance' columns to plot, you can do the following:
    temperature_data = df['Temperature']
    resistance_data = df['Resistance']

    # Clear the previous plot (if any) and plot the new data
    plt.cla()
    plt.plot(temperature_data, resistance_data)

    plt.title('Temperature vs. Resistance')
    plt.xlabel('Temperature (Kelvin)')
    plt.ylabel('Resistance (Ohms)')

    # Additional plot settings, labels, etc., can be added here
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
    #print(df)
    
    ani = animation.FuncAnimation(plt.gcf(), animate, frames=len(df), interval=1000)
    plt.show()
