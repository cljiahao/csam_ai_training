import cv2
import numpy as np
from PIL import Image
from cv2.typing import RotatedRect

from utils.image_process.blob_handler import BlobHandler


class ChipProcessor:
    """A utility class for processing images related to chips.

    Args:
        mask_image (np.ndarray): The threshold mask image for the chip mask.
        border_pad (int): The padding to apply around the chip before cropping.
        chip_noise_erode (int): The erosion size for the noise removal chip mask.
        chip_dilate (int): The dilation size for the chip mask.
        chip_erode (int): The erosion size for the chip mask.
        crop_size (int): The size of the crop after rotation.

    Attributes:
        border_pad (int): The padding applied to the image border before cropping.
        crop_size (int): The size to which the chips should be cropped after rotation.
        chip_mask (np.ndarray): The processed chip mask after applying morphological operations.
    """

    def __init__(
        self,
        mask_image: np.ndarray,
        border_pad: int,
        chip_noise_erode: int,
        chip_dilate: int,
        chip_erode: int,
        crop_size: int,
    ) -> None:
        self.border_pad = border_pad
        self.crop_size = crop_size
        self.chip_mask = self.apply_morphology(
            mask_image, chip_noise_erode, chip_dilate, chip_erode
        )

    @staticmethod
    def apply_morphology(
        mask_image: np.ndarray,
        chip_noise_erode: int,
        chip_dilate: int,
        chip_erode: int,
    ):
        """Applies morphological operations to the binary mask."""
        noised_removed = cv2.erode(
            mask_image, np.ones((chip_noise_erode, chip_noise_erode), np.uint8)
        )
        dilated_image = cv2.dilate(
            noised_removed, np.ones((chip_dilate, chip_dilate), np.uint8)
        )
        eroded_image = cv2.erode(
            dilated_image, np.ones((chip_erode, chip_erode), np.uint8)
        )

        return eroded_image

    def rotate_chips(
        self,
        image: np.ndarray,
        rect: RotatedRect,
    ) -> np.ndarray:
        """Return rotated image cropped to specified size."""

        ((x_center, y_center), (width, height), theta) = rect
        if height < width:
            theta -= 90

        pre_crop_image = BlobHandler.crop_roi(
            image, x_center, y_center, self.border_pad
        )

        pil_image = Image.fromarray(pre_crop_image)
        rotated_image = np.asarray(pil_image.rotate(theta))

        rotated_crop_image = BlobHandler.crop_roi(
            rotated_image, self.border_pad, self.border_pad, self.crop_size // 2
        )

        return rotated_crop_image
