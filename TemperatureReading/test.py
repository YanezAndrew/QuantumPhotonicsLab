import pandas as pd
import matplotlib.pyplot as plt

# Set the figure size
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

# Make a list of columns
columns = ['Timestamp', 'Temp']

# Read a CSV file
df = pd.read_csv("test.csv", usecols=columns)

# Convert 'Timestamp' column to datetime
df['Timestamp'] = pd.to_datetime(df['Timestamp'], format="%a %b %d %H:%M:%S %Y")

# Plot the points on the line
plt.plot(df['Timestamp'], df['Temp'], '-o')

plt.show()