import plot
import extract_data

import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime


def setup_results_table():
    ''' Gives statistics on the bad components of a tile based on all tests completed
    '''
    # TODO - Give reference in docstring about why table is created w/ 0's then updated

    fig_results = plt.figure(figsize=(8, 2.5), num='Bad Components')
    results_table = fig_results.add_subplot(212)
    analysis_text = fig_results.add_subplot(211)

    # Plot will be displayed with the table if this isn't done
    results_table.axis('off')
    analysis_text.axis('off')
    plt.subplots_adjust(left=0.3)

    # TODO - Change to tuples
    # Column and row labels for table
    columns = ["Bad Chips", "Bad Columns", "Bad Pixels"]
    rows = ["Mean Total", "Lower Than Threshold", "Higher Than Threshold",
            "Standard Deviation Total", "Lower Than Threshold", "Higher Than Threshold",
            "Overall Total"]
    # Only need 16 bit ints as max value of an array element will be 4096
    table_values = np.zeros((7, 3), dtype=np.int16)

    # TODO - Is loc argument needed?
    # Create table ready to be updated upon analysis
    results_table = plt.table(cellText=table_values, rowLabels=rows, colLabels=columns, loc="upper center")

    return (fig_results, results_table, analysis_text)


def update_table(table_values, results_table):
    ''' Update values in results table - values may change between each analysis if file chosen is
        different each time
    '''

    # Get dictionary of cells in table
    cells_dict = results_table.get_celld()

    for row in range(0, len(table_values)):
        for col in range(0, len(table_values[row])):
            # row + 1 is used to avoid manipulating column headers
            cells_dict[(row + 1, col)].get_text().set_text(table_values[row][col])

    # TODO - Does table need to be returned?
    return results_table


def set_analysis_text(analysis_text, filename, data_path):
    # Get the date the data file was last modified
    date_modified = os.path.getmtime(data_path + filename)

    analysis_date = datetime.today().strftime('%d/%m/%Y')

    # Used an implicitly joined string as multilines have indentation when formatted to PEP8
    analysis_metadata = ("Data file used: {}".format(filename),
                         "Date modified of data: {}".format(date_modified),
                         "Date of analysis: {}".format(analysis_date))

    for line, line_num in zip(analysis_metadata, range(0, len(analysis_metadata))):
        analysis_text.text(-0.45, (-1.1 + (0.15 * line_num)), line)


def collate_results(bad_chips_mean, bad_chips_stdev, bad_cols_mean, bad_cols_stdev,
                    bad_pixels_mean, bad_pixels_stdev):
    # TODO - Add docstring

    # Totalling all bad components from mean tile
    bad_chips_mean_total = sum(bad_chips_mean)
    bad_cols_mean_total = sum(bad_cols_mean)
    bad_pixels_mean_total = sum(bad_pixels_mean)

    # Totalling all bad components from stdev tile
    bad_chips_stdev_total = sum(bad_chips_stdev)
    bad_cols_stdev_total = sum(bad_cols_stdev)
    bad_pixels_stdev_total = sum(bad_pixels_stdev)

    # Totalling faults of each type of component (chip, column, pixel)
    bad_chips_total = bad_chips_mean_total + bad_chips_stdev_total
    bad_cols_total = bad_cols_mean_total + bad_cols_stdev_total
    bad_pixels_total = bad_pixels_mean_total + bad_pixels_stdev_total

    # TODO - Resolve styling issue
    results_list = [
                    [bad_chips_mean_total, bad_cols_mean_total, bad_pixels_mean_total],
                    [bad_chips_mean[0], bad_cols_mean[0], bad_pixels_mean[0]],
                    [bad_chips_mean[1], bad_chips_mean[1], bad_chips_mean[1]],
                    [bad_chips_stdev_total, bad_cols_stdev_total, bad_pixels_stdev_total],
                    [bad_chips_stdev[0], bad_cols_stdev[0], bad_pixels_stdev[0]],
                    [bad_chips_stdev[1], bad_cols_stdev[1], bad_pixels_stdev[1]],
                    [bad_chips_total, bad_cols_total, bad_pixels_total]
                   ]

    return results_list


def display_trigger_images(lpd_data, tile_position, fig_trigger, trigger_plots, trigger_colorbar):
    ''' Display an image of each of the first 4 triggers (images 1, 11, 21, 31) dependent on
        status of checkbox
    '''

    display_images = (0, 10, 20, 30)

    # Create each trigger image
    for trigger_pos in range(0, 4):
        tile = extract_data.get_single_tile(lpd_data, tile_position, display_images[trigger_pos])

        # Only pass a colorbar once to display_data_plot() - all 4 plots share one colorbar
        if trigger_pos is 3:
            plot.display_data_plot(trigger_plots[trigger_pos], tile, trigger_colorbar)
        else:
            plot.display_data_plot(trigger_plots[trigger_pos], tile)


def display_first_image(lpd_data, first_image_plot, first_image_colorbar):
    ''' Display first image to user dependent on status of checkbox
    '''
    # Get first image of data and plot it
    first_image = extract_data.get_first_image(lpd_data)
    plot.display_data_plot(first_image_plot, first_image, first_image_colorbar)
