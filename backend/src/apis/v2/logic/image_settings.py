import math
import numpy as np
from dataclasses import asdict
from fastapi import UploadFile
from sqlalchemy.orm import Session

from apis.v2.components.utils_image_process import (
    convert_white_bg_to_gray_to_binary,
    create_contour_list,
)
from apis.v2.components.process_batch import (
    apply_morphology_for_batch,
    batch_contours_clean,
    create_batch_coordinates,
)
from apis.v2.components.process_chips import (
    apply_morphology_for_chips,
    chip_crop_finder,
    extract_chip_coordinates,
    find_black_contours,
)
from apis.v2.schemas.image_settings import (
    BatchSettingsData,
    ChipCoordinates,
    ChipSettingsData,
    SettingsCoordinates,
)
from core.logging import logger
from db.services.image_settings import ImageSettingsService
from schemas.contours import ContourInfoList
from utils.debug import timer
from utils.image_process.border_creator import BorderCreator
from utils.image_process.image_manager import ImageManager


def auto_settings_finder(
    item: str, target_count: int, file: UploadFile, db: Session, is_batch: bool
) -> list[ChipCoordinates]:
    """Finds optimal image processing settings and chip coordinates automatically."""
    image = ImageManager.file_to_image(file)
    border_image = BorderCreator.create_border_image(image)
    binary_image = convert_white_bg_to_gray_to_binary(border_image)

    if is_batch:
        settings_data, settings_coordinates = auto_batch_settings_finder(
            binary_image, target_count
        )
    else:
        settings_data, settings_coordinates = auto_chips_settings_finder(
            binary_image, border_image, target_count
        )

    image_settings_service = ImageSettingsService(db)
    image_settings_service.create_or_update_image_settings(item, asdict(settings_data))

    return SettingsCoordinates(coordinates=settings_coordinates)


@timer("Batch Settings Finder")
def auto_batch_settings_finder(
    binary_image: np.ndarray, target_count: int
) -> tuple[BatchSettingsData, list[ChipCoordinates]]:
    """Finds optimal batch processing settings."""
    for erode_value in range(2, 20):
        for close_value in range(2, 20):
            mask_batch = apply_morphology_for_batch(
                binary_image, erode_value, close_value
            )

            contour_info_list = create_contour_list(mask_batch)
            refined_contour_list = batch_contours_clean(contour_info_list)

            count_diff = tabulate_count(refined_contour_list, target_count)
            if count_diff > 0:
                break
            if count_diff == 0:
                logger.info(
                    f"Best Parameter found for Batch - "
                    f"Erode : [{erode_value},{erode_value}], "
                    f"Close : [{close_value},{close_value}]"
                )

                batch_settings_data = BatchSettingsData(
                    batch_erode=erode_value, batch_close=close_value
                )
                batch_coordinates = create_batch_coordinates(
                    refined_contour_list, binary_image
                )
                return batch_settings_data, batch_coordinates
    raise ValueError(f"Unable to match {target_count} for Batch in image")


@timer("Chip Settings Finder")
def auto_chips_settings_finder(
    binary_image: np.ndarray, image: np.ndarray, target_count: int
) -> tuple[ChipSettingsData, list[ChipCoordinates]]:
    """Finds optimal chip processing settings."""
    black_contour_info_list = find_black_contours(image)
    for noise_erode_value in range(1, 20):
        for dilate_value in range(1, 20):
            for erode_value in range(1, 20):
                mask_chip = apply_morphology_for_chips(
                    binary_image, noise_erode_value, dilate_value, erode_value
                )

                contour_info_list = create_contour_list(mask_chip)
                refined_contour_list = chip_crop_finder(
                    contour_info_list, black_contour_info_list, image
                )

                count_diff = tabulate_count(refined_contour_list, target_count)
                if count_diff > 0:
                    break
                if count_diff == 0:
                    logger.info(
                        f"Best Parameter found for Chip - "
                        f"Noise Erode : [{noise_erode_value},{noise_erode_value}], "
                        f"Close : [{dilate_value},{dilate_value}], "
                        f"Erode : [{erode_value},{erode_value}]"
                    )

                    chip_settings_data = ChipSettingsData(
                        chip_noise_erode=noise_erode_value,
                        chip_dilate=dilate_value,
                        chip_erode=erode_value,
                        crop_size=math.ceil(contour_info_list.get_average_length() * 2),
                    )
                    chip_coordinates = extract_chip_coordinates(
                        refined_contour_list, binary_image
                    )
                    return chip_settings_data, chip_coordinates
    raise ValueError(f"Unable to match {target_count} for Chip in image")


def tabulate_count(contour_info_list: ContourInfoList, target_count: int) -> int:
    """Calculates the difference between the target count and the current number of contours."""
    current_count = len(contour_info_list.contours)
    logger.debug(f"Current Count - {current_count} / {target_count}")
    count_diff = target_count - current_count
    return count_diff


def get_image_settings_by_item(item: str, db: Session) -> dict[str, str]:
    """Retrieve image settings from database and return in a dict."""
    image_settings_service = ImageSettingsService(db)
    image_settings = image_settings_service.read_image_settings_not_empty(item)
    return {
        "batch_erode": image_settings.batch_erode,
        "batch_close": image_settings.batch_close,
        "chip_noise_erode": image_settings.chip_noise_erode,
        "chip_dilate": image_settings.chip_dilate,
        "chip_erode": image_settings.chip_erode,
        "crop_size": image_settings.crop_size,
    }
