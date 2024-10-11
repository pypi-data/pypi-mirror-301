import matplotlib.pyplot as plt
import numpy as np

def create_plot(x_range, function):
    x = np.linspace(x_range[0], x_range[1], 100)
    y = function(x)

    plt.plot(x, y)
    plt.title(f'Grafik Fungsi y = {function.__name__}(x)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

