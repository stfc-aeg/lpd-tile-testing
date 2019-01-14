''' Creates plots based on input data
'''

import matplotlib.pyplot as plt
import time

class plot_data_container():
    def __init__(self, figure, ax):
        pass

def display_data_plot(ax, data, colorbar=None, fault_colorbar=False):
    ''' Displays plot of entire images and tiles
        Colorbar isn't required - trigger images share one colorbar 
    '''

    # Specify colorbar ticks and determine max value of data
    if fault_colorbar is False:
        c_ticks = [0, 511, 1023, 1535, 2047, 2559, 3071, 3583, 4095]
    else: 
        c_ticks = [0, 1, 2, 3]

    ax.axis('off')
    image = ax.imshow(data, cmap='ocean', vmin=0, vmax=c_ticks[-1])

    if colorbar is not None:
        # Create and add colorbar
        cbar = plt.colorbar(image, cax=colorbar)
        cbar.set_ticks(ticks=c_ticks)
    
    rows = data.shape[0]
    cols = data.shape[1]
    # Add vertical and horizontal lines to differentiate between chips and tiles
    for i in range(16, cols, 16):
        ax.vlines(i-0.5, 0, rows-1, color='k', linestyles='solid')
        # Add vertical lines to differentiate between tiles
        ax.vlines(128-0.5, 0, rows-1, color='k', linestyle='solid')

    for i in range(32, rows, 32):
        ax.hlines(i-0.5, 0, rows-1, color='k', linestyles='solid')


def display_histogram(ax, data):
    ax.hist(data.flatten(), bins=250)


def clear_screen():
    plt.close()