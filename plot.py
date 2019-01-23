''' Creates plots based on input data
'''

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import matplotlib.colors as colors
import numpy as np


def setup_test_plots(test_type):
    gs1 = gridspec.GridSpec(2, 1, hspace=0.3)
    # GridSpec inside subplot - used for plot of tile with colorbar
    gs1_tile = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gs1[0], wspace=0.05,
                                                width_ratios=[16, 1])

    # Create figure and all subplots
    fig = plt.figure(figsize=(8, 4))
    tile_plot = fig.add_subplot(gs1_tile[0, 0])
    tile_colorbar = fig.add_subplot(gs1_tile[0, 1])
    histogram = fig.add_subplot(gs1[1, 0])

    disable_ticks(tile_plot)
    disable_ticks(tile_colorbar)

    if test_type == 1:
        title_text = "Mean"
    elif test_type == 2:
        title_text = "Standard Deviation"
    else:
        # In case of incorrect test_type argument passed in
        title_text = "Unknown"

    # Add titles
    tile_plot.set_title("Plot of Tile Using {} Data".format(title_text), fontsize=16)
    histogram.set_title("Histogram of {} Tile Data".format(title_text), fontsize=16)

    return (fig, tile_plot, tile_colorbar, histogram)


def setup_fault_plots():
    fig_fault = plt.figure(figsize=(8, 2))
    gs1 = gridspec.GridSpec(1, 2, width_ratios=[16, 1], wspace=0.5)

    fault_tile_plot = fig_fault.add_subplot(gs1[0, 0])
    fault_legend = fig_fault.add_subplot(gs1[0, 1])

    # Disabling axes details for legend and tile plot
    fault_legend.axis('off')
    disable_ticks(fault_tile_plot)

    # Getting range of colour values used in colormap
    cmap = cm.get_cmap('jet')
    colorbar_range = colors.Normalize(vmin=0, vmax=2)

    # Creating legend
    no_fault_patch = mpatches.Patch(color=cmap(colorbar_range(0)), label='No Fault')
    mean_patch = mpatches.Patch(color=cmap(colorbar_range(1)), label='Mean Fault')
    stdev_patch = mpatches.Patch(color=cmap(colorbar_range(2)), label='Stdev Fault')
    fault_legend.legend(handles=[no_fault_patch, mean_patch, stdev_patch], loc='right')

    fault_tile_plot.set_title("Plot of Tile's Faults", fontsize=16)

    return (fig_fault, fault_tile_plot, fault_legend)


def setup_trigger_plots():
    fig_trigger = plt.figure(figsize=(8, 4))
    gs_trigger = gridspec.GridSpec(2, 3, width_ratios=[9, 9, 1])

    # List containing each subplot containing each trigger plot
    trigger_plots = []

    # Coords. of subplots GridSpec positioning
    plot_pos_x = (0, 0, 1, 1)
    plot_pos_y = (0, 1, 0, 1)

    # Create each trigger image
    for trigger_pos in range(0, 4):
        trigger_plots.append(fig_trigger.add_subplot(gs_trigger[plot_pos_x[trigger_pos],
                                                                plot_pos_y[trigger_pos]]))
        trigger_plots[trigger_pos].set_title("Trigger {}".format(trigger_pos + 1))

        # Disable ticks for each trigger tile
        disable_ticks(trigger_plots[trigger_pos])

    trigger_colorbar = fig_trigger.add_subplot(gs_trigger[:, 2])

    fig_trigger.suptitle("First {} Trigger Images".format(len(trigger_plots)), fontsize=16)

    return (fig_trigger, trigger_plots, trigger_colorbar)


def setup_first_image_plot():
    fig_first_image = plt.figure(figsize=(8, 8))
    gs_first_image = gridspec.GridSpec(1, 2, width_ratios=[10, 1])

    # Create subplots for image and respective colorbar
    first_image_plot = fig_first_image.add_subplot(gs_first_image[0, 0])
    first_image_colorbar = fig_first_image.add_subplot(gs_first_image[0, 1])
    first_image_plot.set_title("First Image of Data", fontsize=14)

    return (fig_first_image, first_image_plot, first_image_colorbar)


def disable_ticks(ax):
    ax.set_xticks([])
    ax.set_yticks([])


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
