import cv2
import numpy as np

from apis.v2.helpers.image_process_utils import (
    create_focus_chip_mask,
    extract_hsv_mask_and_area_sum,
    get_largest_info_and_mask,
)
from constants.colors import CSAMcolor
from constants.image_thresholds import AugmentThreshold
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
        _, binary_area_sum = extract_hsv_mask_and_area_sum(major_binary_roi)

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

        defect_mask, defect_area_sum = extract_hsv_mask_and_area_sum(major_defect_roi)

        defect_image = cv2.bitwise_and(rotated_image, rotated_image, mask=defect_mask)
        defect_color = self._get_defect_color(defect_image)

        defect_size = self._determine_size(
            defect_area_sum, major_defect_contour_info.area
        )

        if defect_color is None or defect_size is None:
            return ClassLabel.OTHERS.value, None, None
        return ClassLabel.NG.value, defect_color, defect_size

    def _get_defect_color(self, defect: np.ndarray) -> str | None:
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

        # Match the high count color to the csam_color dictionary adn return color type
        return next(
            (
                csam_color.value.name
                for csam_color in CSAMcolor
                if np.array_equal(csam_color.value.bgr, most_common_color)
            ),
            None,
        )

    def _determine_size(self, area_sum: float, defect_area: float) -> str | None:
        """Determines the size classification based on the area ratio."""
        size_ratio = round(area_sum / defect_area * 100, 2)

        if size_ratio == 0:
            return None
        elif size_ratio < AugmentThreshold.SMALL_SIZE_THRESHOLD.value:
            return "small"
        elif size_ratio > AugmentThreshold.BIG_SIZE_THRESHOLD.value:
            return "big"
        return "medium"
