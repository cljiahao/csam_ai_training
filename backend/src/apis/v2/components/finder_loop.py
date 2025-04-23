import math
import numpy as np

from apis.v2.helpers.image_process_utils import (
    check_single,
    create_contour_list,
)
from apis.v2.helpers.processor.batch_processor import BatchProcessor
from apis.v2.helpers.processor.chip_processor import ChipProcessor
from constants.chip_thresholds import ChipThreshold
from core.logging import logger
from schemas.contours import ContourList
from utils.debug import timer


@timer("Auto Batch Settings Finder Loop")
def batch_finder(
    binary_image: np.ndarray, target_count: int
) -> tuple[int, int, ContourList]:
    for erode_value in range(2, 50):
        for close_value in range(2, 50):
            batch_mask = BatchProcessor.apply_morphology(
                binary_image, erode_value, close_value
            )

            contour_info_list = create_contour_list(batch_mask)

            refined_contour_list = batch_contours_clean(contour_info_list)

            count_diff = tabulate_count(refined_contour_list, target_count)
            if count_diff > 0:
                break
            if count_diff == 0:
                logger.info(
                    f"Best Parameter found for Batch - Erode : [{erode_value},{erode_value}], Close : [{close_value},{close_value}]"
                )

                return (
                    erode_value,
                    close_value,
                    refined_contour_list,
                )

    raise ValueError(f"Unable to match {target_count} for Batch in image")


def batch_contours_clean(
    contour_info_list: ContourList,
):
    avg_contour_area = contour_info_list.get_median_area()
    same_size_contours = [
        contour_info
        for contour_info in contour_info_list.contours
        if avg_contour_area * 0.5 < contour_info.area
    ]
    return ContourList(contours=same_size_contours)


@timer("Auto Chip Settings Finder Loop")
def chip_finder(
    binary_image: np.ndarray, border_blank: np.ndarray, target_count: int
) -> tuple[int, int, int, ContourList]:
    for noise_erode_value in range(1, 50):
        for dilate_value in range(1, 50):
            for erode_value in range(1, 50):
                chip_mask = ChipProcessor.apply_morphology(
                    binary_image, noise_erode_value, dilate_value, erode_value
                )

                contour_info_list = create_contour_list(chip_mask)
                if not contour_info_list:
                    continue
                refined_contour_list = chip_crop_finder(contour_info_list, border_blank)

                count_diff = tabulate_count(refined_contour_list, target_count)
                if count_diff > 0:
                    break
                if count_diff == 0:
                    logger.info(
                        f"Best Parameter found for Chip - Noise Erode : [{noise_erode_value},{noise_erode_value}], Close : [{dilate_value},{dilate_value}], Erode : [{erode_value},{erode_value}]"
                    )

                    return (
                        noise_erode_value,
                        dilate_value,
                        erode_value,
                        refined_contour_list,
                    )

    raise ValueError(f"Unable to match {target_count} for Chip in image")


def chip_crop_finder(
    contour_info_list: ContourList,
    border_blank: np.ndarray,
) -> ContourList:

    median_area = contour_info_list.get_median_area()
    chip_threshold = ChipThreshold()
    chip_threshold.apply_ratios(median_area)

    average_length = contour_info_list.get_average_length()
    crop_size = math.ceil(average_length * 2)

    refined_contours = [
        split_contour
        for contour_info in contour_info_list.contours
        for split_contour in check_single(
            contour_info,
            border_blank,
            crop_size,
            chip_threshold.UPPER_CHIP_AREA,
        ).contours
    ]

    return ContourList(contours=refined_contours)


def tabulate_count(contour_list: ContourList, target_count: int) -> int:
    current_count = len(contour_list.contours)
    logger.debug(f"Current Count - {current_count} / {target_count}")
    count_diff = target_count - current_count
    return count_diff
