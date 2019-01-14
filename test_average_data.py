import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import matplotlib.gridspec as gridspec
import numpy as np

import plot
import extract_data
import fault_tiles

def bad_chips(mean_tile, fault_tile):
    chip_threshold = [3148.428, 3639.3864]
    below_threshold_chips = 0
    above_threshold_chips = 0
    
    for chip in range(0, 8):
        # Calculate the mean of each chip, slicing each chip from mean_tile
        # Values stored in a list - might be useful for later on
        fault_chip = extract_data.get_single_chip(fault_tile, chip)
        test_chip = fault_tiles.detect(fault_chip)

        if test_chip:
            mean_chip_value = np.mean(extract_data.get_single_chip(mean_tile, chip))

            if mean_chip_value < chip_threshold[0]:
                below_threshold_chips += 1
                chip_position = chip * 16
                fault_tiles.add_fault(fault_tile, 1, 0, chip_position, (32, chip_position + 16))
            elif mean_chip_value > chip_threshold[1]:
                above_threshold_chips += 1
                chip_position = chip * 16
                fault_tiles.add_fault(fault_tile, 1, 0, chip_position, (32, chip_position + 16))


def bad_columns(mean_tile, fault_tile):
    column_threshold = [3148.428, 3639.3864]
    below_threshold_columns = 0
    above_threshold_columns = 0

    for column in range(0, 128):
        fault_column = extract_data.get_single_column(fault_tile, column)
        test_column = fault_tiles.detect(fault_column)
        if test_column:
            mean_column_value = np.mean(extract_data.get_single_column(mean_tile, column))
            if mean_column_value < column_threshold[0]:
                below_threshold_columns += 1
                fault_tiles.add_fault(fault_tile, 1, 0, column, (32, column + 1))
            elif mean_column_value > column_threshold[1]:
                above_threshold_columns += 1
                fault_tiles.add_fault(fault_tile, 1, 0, column, (32, column + 1))
 

def bad_pixels(mean_tile, fault_tile):
    pixel_threshold = [3148.428, 3639.3864]
    above_threshold_pixels = 0
    below_threshold_pixels = 0

    for i in range(0, len(mean_tile)):
        for j in range(0, len(mean_tile[i])):
            # Might be useful to know if pixels are below or above the threshold
            # Hence separate if statements for the time being

            if fault_tile[i][j] == 0:
                if mean_tile[i][j] < pixel_threshold[0]:
                    below_threshold_pixels += 1
                    fault_tiles.add_fault(fault_tile, 1, i, j)
                elif mean_tile[i][j] > pixel_threshold[1]:
                    above_threshold_pixels += 1
                    fault_tiles.add_fault(fault_tile, 1, i, j)

def manage_figure(mean_tile):
    ''' Executed at the end of the average test to display relevant plots
    '''

    gs1 = gridspec.GridSpec(2, 1, hspace=0.2)
    gs1_tile = gridspec.GridSpecFromSubplotSpec(1, 2, subplot_spec=gs1[0], wspace=0.05, 
                                                width_ratios=[16, 1])

    # Create figure and all subplots
    fig_average = plt.figure(figsize=(12, 6))
    mean_tile_plot = fig_average.add_subplot(gs1_tile[0, 0])
    mean_tile_colorbar = fig_average.add_subplot(gs1_tile[0, 1])
    mean_histogram = fig_average.add_subplot(gs1[1, 0])

    # Add titles
    mean_tile_plot.set_title("Plot of an Average Tile", fontsize=16)
    mean_histogram.set_title("Histogram of Average Tile", fontsize=16)

    plot.display_data_plot(mean_tile_plot, mean_tile, mean_tile_colorbar)
    plot.display_histogram(mean_histogram, mean_tile)

    plt.show()
