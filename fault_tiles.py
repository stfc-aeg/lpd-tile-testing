import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
import matplotlib.cm as cm
import matplotlib.colors as colors

import plot


def add_fault(fault_tile, test_type, x, y, end_points=None):
    '''
    test_type should only be 1 or 2 - any other value that's passed will be ignored
        1 - The test type is a test using mean data
        2 - The type type is a test using standard deviation data
    Only pass end_points (tuple) if you want to add a fault to a section (column or chip)
    '''
    if end_points is None:
        # Used when adding a pixel fault as endpoints are always 1 above the actual pixel fault
        end_points = (x + 1, y + 1)

    if test_type == 1:
        # Mean fault
        fault_tile[x:end_points[0], y:end_points[1]] = 1
    elif test_type == 2:
        # Stdev fault
        fault_tile[x:end_points[0], y:end_points[1]] = 2


def detect(tile_section, test_type):
    ''' Determines whether the data being passed in should be tested or not
        tile_section can be a column or chip section from a tile
    '''
    # Assume the section should be tested and attempt to prove it shouldn't
    test_section = True

    # Counts the number of bad pixels in the given area
    fault_count = 0

    # Count number of faulty pixels in section
    for i in range(0, len(tile_section)):
        for j in range(0, len(tile_section[i])):
            if tile_section[i][j] != 0:
                fault_count += 1

    num_pixels = len(tile_section[0])

    # If majority of section is faulty, don't test it
    if (fault_count / num_pixels) * 100 > 90:
        test_section = False

    return test_section


def plot_faults(fault_tile):
    ''' Plot all the faults found during testing the tile
    '''
    gs1 = gridspec.GridSpec(1, 2, width_ratios=[16, 1], wspace=0.3)
    fig_fault = plt.figure(figsize=(12, 3))

    fault_tile_plot = fig_fault.add_subplot(gs1[0, 0])
    fault_legend = fig_fault.add_subplot(gs1[0, 1])

    # Disabling axes for legend
    fault_legend.axis('off')

    plot.display_data_plot(fault_tile_plot, fault_tile, colorbar_type=2)

    # Getting range of colour values used in colormap
    cmap = cm.get_cmap('jet')
    colorbar_range = colors.Normalize(vmin=0, vmax=2)

    # Creating legend
    no_fault_patch = mpatches.Patch(color=cmap(colorbar_range(0)), label='No Fault')
    mean_patch = mpatches.Patch(color=cmap(colorbar_range(1)), label='Mean Fault')
    stdev_patch = mpatches.Patch(color=cmap(colorbar_range(2)), label='Stdev Fault')
    fault_legend.legend(handles=[no_fault_patch, mean_patch, stdev_patch], loc='upper right')

    fault_tile_plot.set_title("Plot of Tile's Faults", fontsize=16)

    plt.show()
