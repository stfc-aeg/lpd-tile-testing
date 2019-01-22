import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

import plot
import extract_data
import fault_tiles


def bad_chips(tile_data, fault_tile, test_type):
    ''' Test number of bad chips based on the input from tile_data
    '''
    # Thresholds used to determine bad chips
    if test_type == 1:
        chip_threshold = (3148.428, 3639.3864)
    elif test_type == 2:
        chip_threshold = (0, 50)  # TODO - Change to stdev values

    below_threshold_chips = 0
    above_threshold_chips = 0

    for chip in range(0, 8):
        # Calculate the mean of each chip, slicing each chip from tile_data
        fault_chip = extract_data.get_single_chip(fault_tile, chip)
        # Determine whether the chip needs testing
        test_chip = fault_tiles.detect(fault_chip, test_type)

        if test_chip:
            mean_chip_value = np.mean(extract_data.get_single_chip(tile_data, chip))

            if mean_chip_value < chip_threshold[0]:
                below_threshold_chips += 1
                chip_position = chip * 16

                # Add fault to tile
                fault_tiles.add_fault(fault_tile, test_type, 0, chip_position, (32, chip_position + 16))
            elif mean_chip_value > chip_threshold[1]:
                above_threshold_chips += 1
                chip_position = chip * 16
                fault_tiles.add_fault(fault_tile, test_type, 0, chip_position, (32, chip_position + 16))

    # Collate results of bad chips to be used in test_results.py
    num_bad_chips = [below_threshold_chips, above_threshold_chips]
    return num_bad_chips


def bad_columns(tile_data, fault_tile, test_type):
    ''' Test number of bad columns based on the input from tile_data
    '''
    if test_type == 1:
        column_threshold = (3148.428, 3639.3864)
    elif test_type == 2:
        column_threshold = (0, 50)    # TODO - Change

    below_threshold_columns = 0
    above_threshold_columns = 0

    for column in range(0, 128):
        fault_column = extract_data.get_single_column(fault_tile, column)
        test_column = fault_tiles.detect(fault_column, test_type)
        if test_column:
            mean_column_value = np.mean(extract_data.get_single_column(tile_data, column))
            if mean_column_value < column_threshold[0]:
                below_threshold_columns += 1
                fault_tiles.add_fault(fault_tile, test_type, 0, column, (32, column + 1))
            elif mean_column_value > column_threshold[1]:
                above_threshold_columns += 1
                fault_tiles.add_fault(fault_tile, test_type, 0, column, (32, column + 1))

    num_bad_cols = [below_threshold_columns, above_threshold_columns]
    return num_bad_cols


def bad_pixels(tile_data, fault_tile, test_type):
    ''' Test number of bad pixels based on the input from tile_data
    '''
    if test_type == 1:
        pixel_threshold = (3148.428, 3639.3864)
    elif test_type == 2:
        pixel_threshold = (0, 50)  # TODO - Change

    above_threshold_pixels = 0
    below_threshold_pixels = 0

    for i in range(0, len(tile_data)):
        for j in range(0, len(tile_data[i])):
            if fault_tile[i][j] == 0:
                if tile_data[i][j] < pixel_threshold[0]:
                    below_threshold_pixels += 1
                    fault_tiles.add_fault(fault_tile, test_type, i, j)
                elif tile_data[i][j] > pixel_threshold[1]:
                    above_threshold_pixels += 1
                    fault_tiles.add_fault(fault_tile, test_type, i, j)

    num_bad_pixels = [below_threshold_pixels, above_threshold_pixels]
    return num_bad_pixels


def manage_figure(tile_data, tile_plot, tile_colorbar, histogram, colorbar_type):
    ''' Executed at the end of the mean test to display relevant plots
    '''

    # Display tile plot and relevant histogram
    plot.display_data_plot(tile_plot, tile_data, tile_colorbar, colorbar_type)
    plot.display_histogram(histogram, tile_data)
