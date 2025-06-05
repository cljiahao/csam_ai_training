import cv2
import numpy as np

from apis.v2.components.utils_image_process import (
    focus_blob_body_mask,
    focus_center_blob,
    get_largest_blob_mask_and_info,
    get_non_red_black_mask_and_area_hsv,
)
from apis.v2.constants.csam_thresholds import DefectSizeThreshold, DefectSizeType
from apis.v2.schemas.common import ChipThreshold
from apis.v2.schemas.csam_image import DefectInfo
from constants.colors import BGRColors, CSAMcolor
from constants.folder_names import BaseSetsFolderName
from schemas.contours import ContourInfo


def classify_non_black_defect_mode(
    chip_threshold: ChipThreshold, contour_info: ContourInfo, image: np.ndarray
) -> DefectInfo:
    """Classifies the defect mode for non-black defects based on area and color."""
    deform_info = deform_chip_condition(chip_threshold, contour_info)
    if deform_info:
        return deform_info

    roi_image = focus_center_blob(image)
    major_roi_mask, largest_contour_info = get_largest_blob_mask_and_info(roi_image)

    good_info = good_chip_condition(image, major_roi_mask)
    if good_info:
        return good_info

    minor_roi_mask = focus_blob_body_mask(major_roi_mask, largest_contour_info)
    minor_roi_image = cv2.bitwise_and(image, image, mask=minor_roi_mask)

    minor_hsv_mask, hsv_area_sum = get_non_red_black_mask_and_area_hsv(minor_roi_image)
    defect_size = determine_defect_size(hsv_area_sum, np.count_nonzero(minor_roi_mask))

    defect_image = cv2.bitwise_and(image, image, mask=minor_hsv_mask)
    defect_color = determine_non_black_defect_color(defect_image)

    if defect_size is None or defect_color is None:
        return DefectInfo(
            label_mode=BaseSetsFolderName.OTHERS,
            defect_size=defect_size,
            defect_color=defect_color,
        )
    return DefectInfo(
        label_mode=BaseSetsFolderName.NG,
        defect_size=defect_size,
        defect_color=defect_color,
    )


def classify_black_defect_mode(
    chip_threshold: ChipThreshold, contour_info: ContourInfo, image: np.ndarray
) -> DefectInfo:
    """Classifies the defect mode specifically for black defects."""
    deform_info = deform_chip_condition(chip_threshold, contour_info)
    if deform_info:
        return deform_info

    roi_image = focus_center_blob(image)
    major_roi_mask, largest_contour_info = get_largest_blob_mask_and_info(roi_image)

    minor_roi_mask = focus_blob_body_mask(major_roi_mask, largest_contour_info)
    ng_black = np.array(BGRColors.BLACK.value)
    black_mask = cv2.inRange(image, ng_black, ng_black)

    defect_size = determine_defect_size(
        np.count_nonzero(black_mask), np.count_nonzero(minor_roi_mask)
    )

    if defect_size == "big":
        label_mode = (
            BaseSetsFolderName.NG if defect_size == "big" else BaseSetsFolderName.OTHERS
        )
    return DefectInfo(
        label_mode=label_mode,
        defect_size=defect_size,
        defect_color=CSAMcolor.BLACK.get_name(),
    )


def deform_chip_condition(
    chip_threshold: ChipThreshold,
    contour_info: ContourInfo,
) -> DefectInfo | None:
    """Condition function to check if chip is deformed."""
    if not (
        chip_threshold.LOWER_DEFECT_AREA
        <= contour_info.area
        <= chip_threshold.UPPER_DEFECT_AREA
    ):
        return DefectInfo(
            label_mode=BaseSetsFolderName.DEFORM, defect_size=None, defect_color=None
        )


def good_chip_condition(image: np.ndarray, mask: np.ndarray) -> DefectInfo | None:
    """Condition function to check if chip is good."""
    roi_image = cv2.bitwise_and(image, image, mask=mask)
    _, hsv_area_sum = get_non_red_black_mask_and_area_hsv(roi_image)
    if hsv_area_sum == 0:
        return DefectInfo(
            label_mode=BaseSetsFolderName.GOOD, defect_size=None, defect_color=None
        )


def determine_defect_size(defect_area: float, base_area: float) -> str | None:
    """Determines the size classification based on the area ratio."""
    if base_area == 0:
        return None

    size_ratio = round(defect_area / base_area * 100, 2)
    if size_ratio == 0:
        return None
    elif size_ratio < DefectSizeThreshold.SMALL:
        return DefectSizeType.SMALL
    elif size_ratio < DefectSizeThreshold.MEDIUM:
        return DefectSizeType.MEDIUM
    return DefectSizeType.BIG


def determine_non_black_defect_color(defect: np.ndarray) -> str | None:
    """Determine the most common color type of a defect, excluding black (outline)."""
    reshaped_defect = defect.reshape(-1, defect.shape[-1])
    color_hexes, hex_count = np.unique(reshaped_defect, axis=0, return_counts=True)

    # Find the index of black color if it exists
    black_bgr = np.array(BGRColors.BLACK.value)
    non_black_indices = [
        i for i, color in enumerate(color_hexes) if not np.array_equal(color, black_bgr)
    ]
    if not non_black_indices:
        return None

    non_black_counts = hex_count[non_black_indices]
    most_common_index = np.argmax(non_black_counts)

    non_black_colors = color_hexes[non_black_indices]
    most_common_color = non_black_colors[most_common_index]
    return next(
        (
            csam_color.get_name()
            for csam_color in CSAMcolor
            if np.array_equal(np.array(csam_color.get_bgr()), most_common_color)
        ),
        None,
    )
