import os
import cv2
import math
import numpy as np

from core.config import settings


def create_border_img(path):
    """
    Parameters
    ----------
    path : string
        Path to image file

    Returns
    -------
    border_img : MatLike
        Border added image
    gray : MatLike
        Gray Image for masking purposes
    [w,h] : list
        Width and height of the image
    """
    image = cv2.imread(path)

    h, w, z = image.shape
    # Added border to include chips near the edge of images,
    # allowing better cropping of chips later on
    padx, pady = [math.ceil(i / 10) * 10 for i in settings.IMAGE_SIZE]
    border_img = cv2.copyMakeBorder(image, pady, pady, padx, padx, cv2.BORDER_REPLICATE)
    img = border_img.copy()

    # Mask for background and convert all to 255 for easier threshold (remove background)
    background = np.where(
        (img[:, :, 0] >= 130) & (img[:, :, 1] >= 130) & (img[:, :, 2] >= 130)
    )
    img[background] = (255, 255, 255)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    return border_img, gray, [w, h]
