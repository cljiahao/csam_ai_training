import cv2
import math
from fastapi import UploadFile
from sqlalchemy.orm import Session

from apis.v2.components.extract_image_coords import (
    extract_batch_coords,
    extract_chip_coords,
)
from apis.v2.components.finder_loop import batch_finder, chip_finder
from apis.v2.helpers.image_process_utils import create_border
from apis.v2.schemas.settings import FileDataLists
from db.services.image_settings import ImageSettingsService
from utils.debug import timer
from utils.image_process.image_manager import ImageManager


@timer("Auto Settings Finder")
def auto_settings_finder(
    item: str, target_count: int, file: UploadFile, db: Session, is_batch: bool
) -> FileDataLists:
    """Finds optimal settings based on the provided image and mode."""

    image = ImageManager.file_to_image(file)

    _, border_gray, border_blank, _ = create_border(image)
    _, binary_image = cv2.threshold(border_gray, 250, 255, cv2.THRESH_BINARY_INV)

    if is_batch:
        erode_value, close_value, contour_info_list = batch_finder(
            binary_image, target_count
        )

        settings_data = {"batch_erode": erode_value, "batch_close": close_value}
    else:
        noise_erode_value, dilate_value, erode_value, contour_info_list = chip_finder(
            binary_image, border_blank, target_count
        )
        settings_data = {
            "chip_noise_erode": noise_erode_value,
            "chip_dilate": dilate_value,
            "chip_erode": erode_value,
            "crop_size": math.ceil(contour_info_list.get_average_length() * 2),
        }

    image_settings_service = ImageSettingsService(db)
    image_settings_service.create_or_update_image_settings(item, settings_data)

    data_list = extract_coords(image.shape[:2], contour_info_list, is_batch)

    return FileDataLists(data_files=data_list)


@timer("Extracting Coordinates")
def extract_coords(image_size: tuple[int, int], contour_info, is_batch: bool) -> list:
    """Extracts batch or chip coordinates based on mode."""
    if is_batch:
        return extract_batch_coords(image_size, contour_info)
    return extract_chip_coords(image_size, contour_info)
