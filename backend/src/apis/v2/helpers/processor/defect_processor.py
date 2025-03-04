import cv2
import numpy as np

from apis.v2.components.extract_roi import (
    get_defect_color,
    create_focus_chip_mask,
    determine_size,
    get_hsv_mask_and_contour_area,
    get_largest_info_and_mask,
)
from constants.tf_model import ClassLabel
from constants.chip_thresholds import ChipThreshold
from interface.image_process import ChipProcessorInterface
from schemas.chips_data import ImageData
from schemas.contours import ContourInfo


class DefectProcessor:
    """A utility class for processing defects in images related to chips, including defect classification and batch processing.

    Args:
        chip_processor (ChipProcessorInterface): The chip processor interface.
        chip_threshold (ChipThreshold): The thresholds for chip defect classification.

    Attributes:
        chip_processor (ChipProcessorInterface): The interface for chip processing.
        chip_threshold (ChipThreshold): The thresholds used to classify defects.
    """

    def __init__(
        self,
        chip_processor: ChipProcessorInterface,
        chip_threshold: ChipThreshold,
    ):
        self.chip_processor: ChipProcessorInterface = chip_processor
        self.chip_threshold: ChipThreshold = chip_threshold

    def process_defects(
        self,
        file_name: str,
        image: np.ndarray,
        contour_info: ContourInfo,
    ) -> ImageData:
        """Processes defects in a chip image by classifying the defect type."""

        rotated_image = self.chip_processor.rotate_chips(image, contour_info.rect)

        label_mode, defect_color, defect_size = self._classify_defect_mode(
            rotated_image, contour_info
        )

        return ImageData(
            file_name=file_name,
            rotated_image=rotated_image,
            label_mode=label_mode,
            defect_color=defect_color,
            defect_size=defect_size,
        )

    def _classify_defect_mode(
        self,
        rotated_image: np.ndarray,
        contour_info: ContourInfo,
    ) -> tuple[str, str | None, str | None]:
        """Classifies defect mode, size and color."""

        if not (
            self.chip_threshold.LOWER_DEFECT_AREA
            <= contour_info.area
            <= self.chip_threshold.UPPER_DEFECT_AREA
        ):
            return ClassLabel.OTHERS.value, None, None

        binary_image = create_focus_chip_mask(rotated_image)
        _, major_binary_mask = get_largest_info_and_mask(binary_image)

        major_binary_roi = cv2.bitwise_and(
            rotated_image, rotated_image, mask=major_binary_mask
        )
        _, binary_area_sum = get_hsv_mask_and_contour_area(major_binary_roi)

        if binary_area_sum == 0:
            return ClassLabel.G.value, None, None

        # TODO: change constant to dynamic? need more study
        morph_open = cv2.morphologyEx(
            binary_image, cv2.MORPH_OPEN, np.ones((13, 7), np.uint8)
        )

        major_defect_contour_info, major_defect_mask = get_largest_info_and_mask(
            morph_open
        )
        major_defect_roi = cv2.bitwise_and(
            rotated_image, rotated_image, mask=major_defect_mask
        )

        defect_mask, defect_area_sum = get_hsv_mask_and_contour_area(major_defect_roi)

        defect_image = cv2.bitwise_and(rotated_image, rotated_image, mask=defect_mask)
        defect_color = get_defect_color(defect_image)

        defect_size = determine_size(defect_area_sum, major_defect_contour_info.area)

        if defect_color is None or defect_size is None:
            return ClassLabel.OTHERS.value, None, None
        return ClassLabel.NG.value, defect_color, defect_size
