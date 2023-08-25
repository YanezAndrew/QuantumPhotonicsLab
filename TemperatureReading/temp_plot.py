import pandas as pd
import matplotlib.pyplot as plt
import ast
import numpy as np

df = pd.read_csv('data_2023-08-24 (7).csv')

plt.plot(df['Temperature'])
plt.show()