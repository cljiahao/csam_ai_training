import cv2
import math
import numpy as np

from apis.v2.helpers.image_process_utils import create_border, create_contour_list
from constants.image_thresholds import AugmentThreshold
from constants.colors import BGRColors, CSAMcolor
from schemas.contours import ContourInfo
from utils.image_process.mask_handler import MaskHandler


def create_focus_chip_mask(image: np.ndarray) -> np.ndarray:
    """Creates a mask of the focus chip area by cropping the image and adding borders."""
    focus_chip_pad = math.floor(image.shape[0] / 4 * 0.7)
    cropped_image = image[
        focus_chip_pad:-focus_chip_pad, focus_chip_pad:-focus_chip_pad
    ]
    _, border_gray, _, _ = create_border(cropped_image, border_pad=focus_chip_pad)
    mask_handler = MaskHandler(border_gray)
    return mask_handler.binary_image


def get_largest_info_and_mask(mask_image: np.ndarray) -> tuple[ContourInfo, np.ndarray]:
    """Finds and returns the largest contour's information and its corresponding mask."""
    contour_info_list = create_contour_list(mask_image)
    largest_contour_info = max(contour_info_list.contours, key=lambda x: x.area)

    largest_mask = np.zeros(mask_image.shape[:2], np.uint8)
    cv2.drawContours(
        largest_mask,
        [largest_contour_info.contour],
        -1,
        BGRColors.WHITE.value,
        -1,
    )

    return largest_contour_info, largest_mask


def get_hsv_mask_and_contour_area(roi_image: np.ndarray) -> tuple[np.ndarray, float]:
    """Returns the HSV mask and the total area of all contours in the given ROI image."""
    hsv = cv2.cvtColor(roi_image, cv2.COLOR_BGR2HSV_FULL)
    hsv_mask = cv2.inRange(hsv, np.array([1, 0, 0]), np.array([254, 255, 255]))

    area_sum = np.count_nonzero(hsv_mask)

    return hsv_mask, area_sum


def determine_size(area_sum: float, defect_area: float) -> str | None:
    """Determines the size classification based on the area ratio."""
    size_ratio = round(area_sum / defect_area * 100, 2)

    if size_ratio == 0:
        size = None
    elif size_ratio < AugmentThreshold.SMALL_SIZE_THRESHOLD.value:
        size = "small"
    elif size_ratio > AugmentThreshold.BIG_SIZE_THRESHOLD.value:
        size = "big"
    else:
        size = "medium"

    return size


def get_defect_color(defect: np.ndarray) -> str | None:
    """Determine the most common color type of a defect, excluding black (background)."""

    color_hexes, hex_count = np.unique(
        defect.reshape(-1, defect.shape[-1]), axis=0, return_counts=True
    )

    # Remove black (background) color
    color_hexes = np.delete(color_hexes, 0, axis=0)
    hex_count = np.delete(hex_count, 0, axis=0)

    if color_hexes.size == 0:
        return None

    # Find the most common color in the defect
    most_common_color = color_hexes[np.argmax(hex_count)]

    # Match the high count color to the csam_color dictionary
    color_type = next(
        (
            csam_color.value.name
            for csam_color in CSAMcolor
            if np.array_equal(csam_color.value.bgr, most_common_color)
        ),
        None,
    )

    return color_type
