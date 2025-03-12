import math
import numpy as np

from apis.v2.helpers.image_process_utils import (
    check_single,
    create_border,
    create_contour_list,
)
from constants.chip_thresholds import ChipThreshold
from core.logging import logger
from schemas.contours import ContourList
from utils.debug import timer
from utils.image_process.mask_handler import MaskHandler


@timer("Auto Batch Setting Finder Loop")
def batch_finder(
    contour_info_list: ContourList,
):
    avg_contour_area = contour_info_list.get_median_area()
    same_size_contours = [
        contours
        for contours in contour_info_list.contours
        if avg_contour_area * 0.5 < contours.area
    ]
    return ContourList(contours=same_size_contours)


@timer("Auto Chip and Crop Setting Finder Loop")
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


def finder_loop(
    image: np.ndarray, target_count: int, is_batch
) -> tuple[int, int, ContourList]:

    _, border_gray, border_blank, _ = create_border(image)

    mask_handler = MaskHandler(border_gray)

    # Parameter Search Loop
    for erode_value in range(2, 50):
        for close_value in range(2, 50):
            mask_image = mask_handler.apply_morphology(erode_value, close_value)

            contour_info_list = create_contour_list(mask_image)

            refined_contour_list = (
                chip_crop_finder(contour_info_list, border_blank)
                if not is_batch
                else batch_finder(contour_info_list)
            )

            current_count = len(refined_contour_list.contours)
            count_diff = target_count - current_count

            if count_diff > 0:
                break
            if count_diff == 0:
                logger.info(
                    f"Best Parameter found for {'Batch' if is_batch else 'Chip'} - Erode : [{erode_value},{erode_value}], Close : [{close_value},{close_value}]"
                )

                return erode_value, close_value, refined_contour_list

    raise ValueError(
        f"Unable to match {target_count} for {'Batch' if is_batch else 'Chip'} in image"
    )
