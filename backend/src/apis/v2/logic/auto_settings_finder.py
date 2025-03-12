import math
from fastapi import UploadFile
from sqlalchemy.orm import Session

from apis.v2.components.extract_image_coords import (
    extract_batch_coords,
    extract_chip_coords,
)
from apis.v2.components.finder_loop import finder_loop
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

    erode_value, close_value, contour_info_list = finder_loop(
        image, target_count, is_batch
    )

    write_to_db(
        db,
        item,
        erode_value,
        close_value,
        contour_info_list.get_average_length(),
        is_batch,
    )

    data_list = extract_coords(image.shape[:2], contour_info_list, is_batch)

    return FileDataLists(data_files=data_list)


@timer("Writing to Database")
def write_to_db(
    db: Session, item: str, erode: int, close: int, average_length: int, is_batch: bool
) -> None:
    """Writes lot and chip details to the database."""

    settings_data = {
        "batch_erode" if is_batch else "chip_erode": erode,
        "batch_close" if is_batch else "chip_close": close,
    }

    if not is_batch and average_length:
        settings_data["crop_size"] = math.ceil(average_length * 2)

    image_settings_service = ImageSettingsService(db)
    image_settings_service.create_or_update_image_settings(item, settings_data)


@timer("Extracting Coordinates")
def extract_coords(image_size: tuple[int, int], contour_info, is_batch: bool) -> list:
    """Extracts batch or chip coordinates based on mode."""
    if is_batch:
        return extract_batch_coords(image_size, contour_info)
    return extract_chip_coords(image_size, contour_info)
