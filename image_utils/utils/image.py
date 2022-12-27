# -*- coding: utf-8 -*-
import numpy as np
from skimage.segmentation import flood_fill


def remove_background(img, threshold=10, init_pos=(0, 0), mode='fill'):
    """ Remove background of img using pixel value from a position

    Parameters
    ----------
    img : ndarray
        Input img.
    threshold : int, optional
        Threshold for background detection in case of noise.
    init_pos : tuple, optional
        Position at which the white vs black background is detected.
    mode : {'fill', 'value'}, optional
        Either replace all close values or use a floodfill.

    Returns
    -------
    new_img : ndarray
        img with background removed.

    """
    shape = img.shape[0:2] + (4,)
    tmp = np.average(img, axis=-1)

    # Black background vs White background
    if tmp[init_pos] < threshold:
        tmp[tmp < threshold] = 0
    elif tmp[init_pos] > 255 - threshold:
        tmp[tmp > 255 - threshold] = 255

    # TODO : Support more than 2 colors
    if mode == 'fill':
        binary_struct = np.zeros((3, 3))
        binary_struct[0:3, 1] = 1
        binary_struct[1, 0:3] = 1

        filled_img = flood_fill(tmp, init_pos, 1000,
                                footprint=binary_struct, tolerance=1)
        filled_img[filled_img != 1000] = 255
        filled_img[filled_img == 1000] = 0
    else:
        filled_img = np.zeros(shape[0:2])
        filled_img[tmp == tmp[threshold]] = -1
        filled_img[tmp != tmp[threshold]] = 255
        filled_img[filled_img == -1] = 0

    # The detected background is used in the Alpha channel
    new_img = np.zeros(shape).astype(np.uint8)
    new_img[:, :, 0:3] = img[:, :, 0:3]
    filled_img = filled_img
    new_img[:, :, 3] = filled_img

    return new_img
