import matplotlib.pyplot as plt
import numpy as np

def create_plot(x_range, function):
    """
    Create a plot of a given function over a specified range.

    Parameters:
    x_range (tuple): A tuple of two values specifying the start and end of the x-axis range.
    function (callable): A function that takes a single argument (x) and returns a value.

    Returns:
    None
    """
    x = np.linspace(x_range[0], x_range[1], 100)
    y = function(x)

    plt.plot(x, y)
    plt.title(f'Grafik Fungsi y = {function.__name__}(x)')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

#contoh penggunaan
# create_plot((0, 2 * np.pi), np.sin)
