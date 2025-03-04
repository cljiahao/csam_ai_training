import numpy as np
from sqlalchemy.orm import Session

from apis.v2.helpers.image_process_utils import (
    check_single,
    create_border,
    create_contour_list,
    get_image_settings,
    process_chip,
)
from apis.v2.helpers.processor.defect_processor import DefectProcessor
from constants.chip_thresholds import ChipThreshold
from schemas.contours import ContourList
from utils.debug import timer
from utils.image_process.mask_handler import MaskHandler


@timer("Process CSAM Image")
def process_csam_image(
    image: np.ndarray, item: str, lot_no: str, plate_no: str, db: Session
) -> tuple[DefectProcessor, str, ContourList, np.ndarray, int]:
    """Main function for processing the input image."""

    # Get crop size settings
    image_settings = get_image_settings(item, db)

    # Border Creation
    border_image, border_gray, border_blank, border_pad = create_border(
        image, crop_size=image_settings.crop_size
    )

    # Mask Processing
    mask_handler = MaskHandler(border_gray)

    # Chip Processing
    chip_processor = process_chip(mask_handler, border_pad, image_settings)

    # Chip Threshold instantiate
    chip_threshold = ChipThreshold()

    refined_contours_info_list = split_and_refine_contours(
        chip_threshold,
        chip_processor.chip_mask,
        border_blank,
        image_settings.crop_size,
    )

    # Defect Processing
    defect_processor = DefectProcessor(chip_processor, chip_threshold)

    base_file_name = f"{lot_no}_{plate_no}"

    return (
        defect_processor,
        base_file_name,
        refined_contours_info_list,
        border_image,
    )


@timer("Split and refining")
def split_and_refine_contours(
    chip_threshold: ChipThreshold,
    chip_mask: np.ndarray,
    blank: np.ndarray,
    crop_size: int,
) -> ContourList:
    """Split and refine contours using BlobHandler."""

    contour_info_list = create_contour_list(chip_mask)

    median_area = contour_info_list.get_median_area()
    chip_threshold.apply_ratios(median_area)

    split_contours = [
        split_contour
        for contour_info in contour_info_list.contours
        for split_contour in check_single(
            contour_info, blank, crop_size, chip_threshold.UPPER_CHIP_AREA
        ).contours
    ]

    refined_contours = [
        contour
        for contour in split_contours
        if chip_threshold.LOWER_CHIP_AREA
        < contour.area
        < chip_threshold.UPPER_CHIP_AREA
    ]

    return ContourList(contours=refined_contours)
