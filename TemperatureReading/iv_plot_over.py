import matplotlib.pyplot as plt
from datetime import datetime
import os
import pandas as pd

# Sample data extracted from the provided line
voltage = [-8.0, -7.111111111111111, -6.222222222222222, -5.333333333333334, -4.444444444444445, -3.5555555555555554, -2.666666666666667, -1.7777777777777786, -0.8888888888888893, 0.0]
current = [-0.00014354539999999997, -0.00012759909999999998, -0.00011164979999999999, -9.570410000000001e-05, -7.973751999999998e-05, -6.379562e-05, -4.7848239999999996e-05, -3.190002e-05, -1.595105e-05, 2.2000000000000003e-09]


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
        plt.figure()
        plt.plot(voltage, current, marker='o', linestyle='-', color='b')
        plt.xlabel('Voltage')
        plt.ylabel('Current')
        plt.title('Current vs. Voltage')
        plt.grid(True)
        plt.tight_layout()
        plt.show()
        