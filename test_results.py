import plot
import extract_data

from IPython.display import HTML, display, update_display
from tabulate import tabulate
import matplotlib.pyplot as plt


def show_test_results(bad_chips_mean, bad_chips_stdev, bad_cols_mean, bad_cols_stdev,
                      bad_pixels_mean, bad_pixels_stdev, results_table):
    ''' Gives statistics on the bad components of a tile based on all tests completed
    '''

    fig_results = plt.figure(figsize=(8, 2), num='Bad Components')
    results_table = fig_results.add_subplot(111)
    results_table.axis('off')

    # When creating the table, just create a numpy array full of zeros
    table_values = update_table_values(bad_chips_mean, bad_chips_stdev,
                                       bad_cols_mean, bad_cols_stdev,
                                       bad_pixels_mean, bad_pixels_stdev)

    columns = ["Bad Chips", "Bad Columns", "Bad Pixels"]
    rows = ["Mean Total", "Lower Than Threshold", "Higher Than Threshold",
            "Standard Deviation Total", "Lower Than Threshold", "Higher Than Threshold",
            "Overall Total"]

    results_table = plt.table(cellText=table_values, rowLabels=rows, colLabels=columns, loc="center")
    plt.subplots_adjust(left=0.3)

    # Undo comment
    return (fig_results, results_table)


def update_table_values(bad_chips_mean, bad_chips_stdev, bad_cols_mean, bad_cols_stdev,
                        bad_pixels_mean, bad_pixels_stdev):
    ''' Update values in results table - values may change between each analysis if file chosen is
        different each time
    '''

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

    table_values = [
                    [bad_chips_mean_total, bad_cols_mean_total, bad_pixels_mean_total],
                    [bad_chips_mean[0], bad_cols_mean[0], bad_pixels_mean[0]],
                    [bad_chips_mean[1], bad_chips_mean[1], bad_chips_mean[1]],
                    [bad_chips_stdev_total, bad_cols_stdev_total, bad_pixels_stdev_total],
                    [bad_chips_stdev[0], bad_cols_stdev[0], bad_pixels_stdev[0]],
                    [bad_chips_stdev[1], bad_cols_stdev[1], bad_pixels_stdev[1]],
                    [bad_chips_total, bad_cols_total, bad_pixels_total]
                   ]

    return table_values


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
