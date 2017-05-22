""" Image utility module. """
from __future__ import absolute_import, division, print_function

import numpy as np


def images_to_sprite(data):
    """Creates the sprite image along with any necessary padding

    Args:
      data: NxHxW[x3] tensor containing the images.

    Returns:
      data: Properly shaped HxWx3 image with any necessary padding.
    """
    print('shape', data.shape)
    if len(data.shape) == 3:
        data = np.tile(data[..., np.newaxis], (1, 1, 1, 3))
    data = data.astype(np.float32)
    minimum = np.min(data.reshape((data.shape[0], -1)), axis=1)
    data = (data.transpose((1, 2, 3, 0)) - minimum).transpose((3, 0, 1, 2))
    maximum = np.max(data.reshape((data.shape[0], -1)), axis=1)
    data = (data.transpose((1, 2, 3, 0)) / maximum).transpose((3, 0, 1, 2))
    # Inverting the colors seems to look better for MNIST
    data = 1 - data

    n = int(np.ceil(np.sqrt(data.shape[0])))
    padding = ((0, n ** 2 - data.shape[0]), (0, 0), (0, 0)) + ((0, 0),) * (data.ndim - 3)
    data = np.pad(data, padding, mode='constant', constant_values=0)
    # Tile the individual thumbnails into an image.
    data = data.reshape((n, n) + data.shape[1:]).transpose(
        (0, 2, 1, 3) + tuple(range(4, data.ndim + 1)))
    data = data.reshape((n * data.shape[1], n * data.shape[3]) + data.shape[4:])
    data = (data * 255).astype(np.uint8)
    return data
