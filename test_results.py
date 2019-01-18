import plot
import extract_data
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from IPython.display import HTML, display
from tabulate import tabulate


def show_test_results(bad_chips_mean, bad_chips_stdev, bad_cols_mean, bad_cols_stdev,
                      bad_pixels_mean, bad_pixels_stdev):
    ''' Gives statistics on the bad components of a tile based on all tests completed
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

    # Outputting faults to user
    table_values = [
                    ["<b>Mean Total</b>", bad_chips_mean_total, bad_cols_mean_total, bad_pixels_mean_total],
                    ["Lower Than Threshold", bad_chips_mean[0], bad_cols_mean[0], bad_pixels_mean[0]],
                    ["Higher Than Threshold", bad_chips_mean[1], bad_chips_mean[1], bad_chips_mean[1]],
                    ["<b>Standard Deviation Total</b>", bad_chips_stdev_total, bad_cols_stdev_total,
                     bad_pixels_stdev_total],
                    ["Lower Than Threshold", bad_chips_stdev[0], bad_cols_stdev[0], bad_pixels_mean[0]],
                    ["Higher Than Threshold", bad_chips_stdev[1], bad_cols_stdev[1], bad_pixels_stdev[1]],
                    ["<b>Overall Total</b>", bad_chips_total, bad_cols_total, bad_pixels_total]
                   ]

    table_headers = ["", "Bad Chips", "Bad Columns", "Bad Pixels"]

    display(HTML(tabulate(table_values, headers=table_headers, tablefmt='html')))


def display_trigger_images(lpd_data, tile_position):
    ''' Display an image of each of the first 4 triggers (images 1, 11, 21, 31) dependent on
        status of checkbox
    '''
    gs_trigger = gridspec.GridSpec(2, 3, width_ratios=[9, 9, 1])
    fig_trigger = plt.figure(figsize=(12, 4))

    # List containing each subplot containing each trigger plot
    trigger_plots = []

    # Coords. of subplots GridSpec positioning
    plot_pos_x = (0, 0, 1, 1)
    plot_pos_y = (0, 1, 0, 1)

    display_images = (0, 10, 20, 30)
    trigger_colorbar = None

    # Create each trigger image
    for trigger_pos in range(0, 4):
        trigger_plots.append(fig_trigger.add_subplot(gs_trigger[plot_pos_x[trigger_pos],
                                                                plot_pos_y[trigger_pos]]))
        tile = extract_data.get_single_tile(lpd_data, tile_position,
                                            display_images[trigger_pos])

        # Only pass a colorbar once to display_data_plot() - all 4 plots share one colorbar
        if trigger_pos is 3:
            trigger_colorbar = fig_trigger.add_subplot(gs_trigger[:, 2])
        plot.display_data_plot(trigger_plots[trigger_pos], tile, trigger_colorbar)
        trigger_plots[trigger_pos].set_title("Trigger {}".format(trigger_pos + 1))

    fig_trigger.suptitle("First {} Trigger Images".format(len(trigger_plots)), fontsize=16)

    plt.show()


def display_first_image(lpd_data):
    ''' Display first image to user dependent on status of checkbox
    '''
    gs_first_image = gridspec.GridSpec(1, 2, width_ratios=[10, 1])
    fig_first_image = plt.figure(figsize=(8, 8))

    # Get first image of data and plot it
    first_image = extract_data.get_first_image(lpd_data)
    first_image_plot = fig_first_image.add_subplot(gs_first_image[0, 0])
    first_image_colorbar = fig_first_image.add_subplot(gs_first_image[0, 1])
    first_image_plot.set_title("First Image of Data", fontsize=14)
    plot.display_data_plot(first_image_plot, first_image, first_image_colorbar)

    plt.show()
