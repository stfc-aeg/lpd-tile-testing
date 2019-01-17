''' Creates plots based on input data
'''

import matplotlib.pyplot as plt
import numpy as np


def display_data_plot(ax, data, colorbar=None, colorbar_type=0):
    ''' Displays plot of entire images and tiles
        Colorbar isn't required so trigger images can share one colorbar
        colorbar_type - int value representing type of colorbar being passed
            0 - Colorbar for image plot using raw or mean data
            1 - Colorbar for image using standard deviation data
            2 - Colorbar for showing tile's faults
    '''
    # Specify colorbar ticks and determine max value of data
    if colorbar_type == 0:
        c_ticks = [0, 511, 1023, 1535, 2047, 2559, 3071, 3583, 4095]
        # Primarily for stdev data that will rarely reach a max of 4095
        data_max = 4095
    elif colorbar_type == 1:
        c_ticks = [0, 511, 1023, 1535, 2047, 2559, 3071, 3583, 4095]
        data_max = np.max(data)
    elif colorbar_type == 2:
        c_ticks = [0, 1, 2]
        # Constant value set for consistency between multiple fault images
        data_max = 2

    # Remove axes of images and create them
    ax.axis('off')
    # Jet colourmap is used in live view section of LPD GUI
    image = ax.imshow(data, cmap='jet', vmin=0, vmax=data_max)

    if colorbar is not None:
        # Create and add colorbar
        cbar = plt.colorbar(image, cax=colorbar)
        cbar.set_ticks(ticks=c_ticks)

        if colorbar_type == 2:
            # Change ticks to strings to make them more understandable to user
            string_ticks = ['No Fault', 'Fault in mean data', 'Fault in stdev. data']
            # set_ticks() is executed before to get 3 ticks, instead of more
            cbar.ax.set_yticklabels(string_ticks)

    rows = data.shape[0]
    cols = data.shape[1]
    # Add vertical and horizontal lines to differentiate between chips and tiles
    for i in range(16, cols, 16):
        ax.vlines(i - 0.5, 0, rows - 1, color='k', linestyles='solid')
        # Add vertical lines to differentiate between tiles
        ax.vlines(128 - 0.5, 0, rows - 1, color='k', linestyle='solid')

    for i in range(32, rows, 32):
        ax.hlines(i - 0.5, 0, rows - 1, color='k', linestyles='solid')


def display_histogram(ax, data):
    ax.hist(data.flatten(), bins=250)


def clear_screen():
    plt.close()
