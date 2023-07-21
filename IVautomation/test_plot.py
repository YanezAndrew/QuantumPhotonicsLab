import numpy as np
import matplotlib.pyplot as plt

points = 10
x = [0.         0.11111111 0.22222222 0.33333333 0.44444444 0.55555556
 0.66666667 0.77777778 0.88888889 1.        ]
y = [-5.559600e-09  1.997699e-06  3.980058e-06  5.982467e-06  7.971581e-06
  9.967398e-06  1.195765e-05  1.394884e-05  1.594532e-05  1.793761e-05]
for i in range(1, points - 1):
    data_string += f",{x[i]:.8f},{y[i]:.8f}"
print(data_string)

#plt.scatter(x, y, s=6)
#plt.title("Diode IV")
#plt.show()

