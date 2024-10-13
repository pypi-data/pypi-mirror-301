# -*- coding: utf-8 -*-
"""*widget_image_display.py* file.

*images* file, from supop_images directory,
that contains functions to process images.

.. module:: supop_images.images
   :synopsis: To complete

.. note:: LEnsE - Institut d'Optique - version 0.1

.. moduleauthor:: Julien VILLEMEJANE <julien.villemejane@institutoptique.fr>
"""
import sys
import cv2
import numpy as np
from PyQt6.QtGui import QImage


def resize_image(im_array: np.ndarray,
                 new_width: int,
                 new_height: int) -> np.ndarray:
    """Resize array containing image at a new size.

    :param im_array: Initial array to resize.
    :type im_array: numpy.ndarray
    :param new_width: Width of the new array.
    :type new_width: int
    :param new_height: Height of the new array.
    :type new_height: int
    :return: Resized array.
    :rtype: numpy.ndarray

    """
    image_rows, image_cols = im_array.shape[:2]
    row_ratio = new_width / float(image_rows)
    col_ratio = new_height / float(image_cols)
    ratio = min(row_ratio, col_ratio)
    resized_image = cv2.resize(im_array,
                               dsize=(new_width, new_height),
                               fx=ratio, fy=ratio,
                               interpolation=cv2.INTER_CUBIC)
    return resized_image

def resize_image_ratio(pixels: np.ndarray, new_height: int, new_width: int) -> np.ndarray:
    """Create a new array with a different size, with the same aspect ratio.

    :param pixels: Array of pixels to resize
    :type pixels: np.ndarray
    :param new_height: New height of the image.
    :type new_height: int
    :param new_width: New width of the image.
    :type new_width: int

    :return: A resized image.
    :rtype: np.ndarray
    """
    height, width = pixels.shape[:2]
    aspect_ratio = width / height

    # Calculate new size with same aspect_ratio
    n_width = new_width
    n_height = int(n_width / aspect_ratio)
    if n_height > new_height:
        n_height = new_height
        n_width = int(n_height * aspect_ratio)
    else:
        n_width = new_width
        n_height = int(n_width / aspect_ratio)
    resized_array = cv2.resize(pixels, (n_width, n_height))
    return resized_array

def array_to_qimage(array: np.ndarray) -> QImage:
    """Transcode an array to a QImage.
    :param array: Array containing image data.
    :type array: numpy.ndarray
    :return: Image to display.
    :rtype: QImage
    """
    shape_size = len(array.shape)
    if shape_size == 2:
        height, width = array.shape
        bytes_per_line = width  # only in 8 bits gray
        return QImage(array, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
    else:
        height, width, _ = array.shape
        bytes_per_line = 3 * width  # only in 8 bits gray
        return QImage(array.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)