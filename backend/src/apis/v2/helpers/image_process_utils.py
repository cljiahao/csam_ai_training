import math
import cv2
import numpy as np
from sqlalchemy.orm import Session

from apis.v2.helpers.processor.chip_processor import ChipProcessor
from constants.colors import BGRColors
from constants.image_thresholds import ImageThreshold
from core.exceptions import MissingSettings
from db.models.image_settings import ImageSettings
from db.services.image_settings import ImageSettingsService
from schemas.contours import ContourInfo, ContourList
from utils.image_process.blob_handler import BlobHandler
from utils.image_process.border_creator import BorderCreator
from utils.image_process.contour_handler import ContourHandler
from utils.image_process.mask_handler import MaskHandler


def get_image_settings(item: str, db: Session) -> ImageSettings:

    image_settings_service = ImageSettingsService(db)
    image_settings = image_settings_service.read_settings(item)

    if image_settings is None:
        raise MissingSettings(
            f"Image settings for '{item}' not found in API or database."
        )

    return image_settings


def create_border(image: np.ndarray, border_pad: int = 0, crop_size: int = 0):
    """Creates border images and returns relevant data."""
    border_creator = BorderCreator(image, border_pad, crop_size)
    border_gray = border_creator.convert_background_white_and_grayscale()
    border_blank = border_creator.create_blank_image()
    border_pad = border_creator.border_pad

    return border_creator.border_image, border_gray, border_blank, border_pad


def create_contour_list(mask_image: np.ndarray) -> ContourList:
    contours, _ = cv2.findContours(
        mask_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    return ContourHandler.filter_and_build_contour_info(
        contours, ImageThreshold.DENOISE_THRESHOLD.value
    )


def process_chip(
    mask_handler: MaskHandler, border_pad: int, image_settings: ImageSettings
):
    """Processes the chip data from the mask handler."""
    chip_processor = ChipProcessor(
        mask_handler,
        image_settings.chip_erode,
        image_settings.chip_close,
        border_pad,
        image_settings.crop_size,
    )
    return chip_processor
def extract_hsv_mask_and_area_sum(image: np.ndarray) -> tuple[np.ndarray, float]:
    """Extracts the HSV mask and calculates the area of all contours in the given image."""
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV_FULL)
    hsv_mask = cv2.inRange(hsv, np.array([1, 0, 0]), np.array([254, 255, 255]))

    area_sum = np.count_nonzero(hsv_mask)

    return hsv_mask, area_sum


def check_single(
    contour_info: ContourInfo,
    blank: np.ndarray,
    crop_size: int,
    check_single_threshold: int = 0,
) -> ContourList:
    """Analyzes a single contour and attempts to split it using erosion."""

    if contour_info.area > check_single_threshold:
        drawn_roi = cv2.drawContours(
            blank.copy(), contour_info.contour, -1, BGRColors.WHITE.value, -1
        )
        ((x_center, y_center), _, _) = contour_info.rect
        crop_image = BlobHandler.crop_roi(drawn_roi, x_center, y_center, crop_size // 2)

        new_contours = BlobHandler.erode_and_find_contours(crop_image)
        if new_contours:
            return ContourHandler.filter_and_build_contour_info(new_contours)

    return ContourList(contours=[contour_info])


def create_focus_chip_mask(image: np.ndarray) -> np.ndarray:
    """Creates a mask of the focus chip area by cropping the image and adding borders."""
    focus_chip_pad = math.floor(image.shape[0] / 4 * 0.7)
    cropped_image = image[
        focus_chip_pad:-focus_chip_pad, focus_chip_pad:-focus_chip_pad
    ]

    _, border_gray, _, _ = create_border(cropped_image, padding=focus_chip_pad)

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
