import matplotlib.pyplot as plt
from datetime import datetime
import os
import pandas as pd

# Sample data extracted from the provided line
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
    #f"data_{current_date} ({cnt - 2}).csv"
    #file_name = "data_2023-08-07 (1).csv"
    file_name = f"data_{current_date} ({cnt - 2}).csv"
    #cnt = 1
    if (cnt == 0):
        print("No File Created For Today or Not in Temperature Reading Directory")
    else:
        file_path = os.path.join(current_dir, file_name)
        print(file_path)
        df = pd.read_csv(file_path)
        voltage = list(df['Voltage'])
        current = list(df['Amps'])
        print(type(voltage))
        print(voltage)
        print(current[0])
        plt.figure()
        for i in range(len(voltage)):
            for j in range(len(voltage[0])):
                plt.scatter(voltage[i][j], current[i][j], marker='o', linestyle='-', color='b')
        plt.xlabel('Voltage')
        plt.ylabel('Current')
        plt.title('Current vs. Voltage')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        