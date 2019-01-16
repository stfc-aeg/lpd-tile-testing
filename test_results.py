import plot
import extract_data
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec


def show_test_results(bad_chips_average, bad_chips_stdev, bad_cols_average, bad_cols_stdev,
                      bad_pixels_average, bad_pixels_stdev):
    ''' Gives statistics on the bad components of a tile based on all tests completed
    '''

    bad_chips_average_total = sum(bad_chips_average)
    bad_cols_average_total = sum(bad_cols_average)
    bad_pixels_average_total = sum(bad_pixels_average)

    bad_chips_stdev_total = sum(bad_chips_stdev)
    bad_cols_stdev_total = sum(bad_cols_stdev)
    bad_pixels_stdev_total = sum(bad_pixels_stdev)

    bad_chips_total = bad_chips_average_total + bad_chips_stdev_total
    bad_cols_total = bad_cols_average_total + bad_cols_stdev_total
    bad_pixels_total = bad_pixels_average_total + bad_pixels_stdev_total

    print("Number of bad chips: {}".format(bad_chips_total))

    print("Bad chips from average data test: {}".format(bad_chips_average_total))
    print("Bad chips from standard deviation test: {}".format(bad_chips_stdev_total))
    print("\n")

    print("Number of bad columns: {}".format(bad_cols_total))
    print("Bad columns from average data test: {}".format(bad_cols_average_total))
    print("Bad columns from standard deviation test: {}".format(bad_cols_stdev_total))
    print("\n")

    print("Number of bad pixels: {}".format(bad_pixels_total))
    print("Bad pixels from average data test: {}".format(bad_pixels_average_total))
    print("Bad pixels from standard deviation test: {}".format(bad_pixels_stdev_total))
    print("\n")


def display_trigger_images(lpd_data, tile_position):
    gs_trigger = gridspec.GridSpec(2, 3, width_ratios=[9, 9, 1])
    fig_trigger = plt.figure(figsize=(12, 4))
    trigger_plots = []
    plot_pos_x = (0, 0, 1, 1)
    plot_pos_y = (0, 1, 0, 1)
    display_images = (0, 10, 20, 30)
    trigger_colorbar = None

    for trigger_pos in range(0, 4):
        trigger_plots.append(fig_trigger.add_subplot(gs_trigger[plot_pos_x[trigger_pos],
                                                                plot_pos_y[trigger_pos]]))
        tile = extract_data.get_single_tile(lpd_data, tile_position,
                                            display_images[trigger_pos])
        if trigger_pos is 3:
            trigger_colorbar = fig_trigger.add_subplot(gs_trigger[:, 2])
        plot.display_data_plot(trigger_plots[trigger_pos], tile, trigger_colorbar)
        trigger_plots[trigger_pos].set_title("Trigger {}".format(trigger_pos + 1))

    fig_trigger.suptitle("First {} Trigger Images".format(len(trigger_plots)), fontsize=16)

    plt.show()


def display_first_image(lpd_data):
    gs_first_image = gridspec.GridSpec(1, 2, width_ratios=[10, 1])
    fig_first_image = plt.figure(figsize=(8, 8))

    first_image = extract_data.get_first_image(lpd_data)
    first_image_plot = fig_first_image.add_subplot(gs_first_image[0, 0])
    first_image_colorbar = fig_first_image.add_subplot(gs_first_image[0, 1])
    first_image_plot.set_title("First Image of Data", fontsize=14)

    plot.display_data_plot(first_image_plot, first_image, first_image_colorbar)

    plt.show()
