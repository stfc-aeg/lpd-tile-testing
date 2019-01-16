''' Extracts data from various places
'''

import h5py
import numpy as np

def get_lpd_data(filename):
    lpd_file = h5py.File(filename, 'r')
    lpd_data = lpd_file['data'][()]
    return lpd_data

def get_first_image(lpd_data):
    single_image = lpd_data[:1,:,:]
    single_image = np.reshape(single_image, (256, 256))
    return single_image

def get_single_tile(lpd_data, tile_position, image_num):
    # Exception will occur if image_num < 0, needs to be caught
    single_tile = lpd_data[image_num:image_num+1, tile_position[0]:tile_position[0] + 32, tile_position[1]:tile_position[1] + 128]
    single_tile = np.reshape(single_tile, (32, 128))
    return single_tile

def get_mean_tile(lpd_data, tile_position):
    tile_data = get_total_tile(lpd_data, tile_position)
    mean_tile = np.mean(tile_data, axis=0)
    return mean_tile

def get_total_tile(lpd_data, tile_position):
    total_tile_data = lpd_data[:lpd_data.shape[0], tile_position[0]:tile_position[0] + 32, tile_position[1]:tile_position[1] + 128]
    return total_tile_data

def get_stdev_image():
    stdev_image = np.std(lpd_data, axis=0)
    return stdev_image

def get_stdev_tile(lpd_data, tile_position):
    tile_data = get_total_tile(lpd_data, tile_position)
    stdev_tile = np.std(tile_data, axis=0)
    return stdev_tile

def get_single_chip(tile, chip_position):
    ''' chip_position - int from 0 to 7
    '''

    chip_position = chip_position * 16
    single_chip = tile[:, chip_position:chip_position + 16]
    return single_chip

def get_single_column(tile, col_position):
    single_column = tile[:, col_position:col_position + 1]
    return single_column

def get_mean_image():
    # Not currently used, is this needed?
    pass

def set_tile_position(tile_orientation, mini_connector):
    ''' Used to set variables defining where to get the data from lpd_data
    ''' 
    tile_position = []

    # Tiles have a 32 pixel height
    tile_position.append(32 * (mini_connector - 1))

    # Left or right tile
    if tile_orientation == "Left Tile":
        # Left tiles are on the RHS of the image, and vice versa
        tile_position.append(128)
    else:
        tile_position.append(0)

    return tile_position