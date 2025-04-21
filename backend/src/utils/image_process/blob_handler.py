import cv2
import numpy as np


class BlobHandler:
    """A utility class for processing blobs (regions of interest) found from contours in images."""

    @staticmethod
    def create_kernel(kernel_size: int) -> np.ndarray:
        """Creates a square kernel of ones for morphological operations.

        Args:
            kernel_size: The size (width and height) of the square kernel.

        Returns:
            A NumPy ndarray representing the square kernel with uint8 data type.
        """
        return np.ones((kernel_size, kernel_size), dtype=np.uint8)

    @staticmethod
    def crop_roi(
        image: np.ndarray, x_center: float, y_center: float, padding: int
    ) -> np.ndarray:
        """Crops a region of interest (ROI) from the given image.

        Args:
            image: The input image.
            x_center: The x-coordinate of the center of the ROI.
            y_center: The y-coordinate of the center of the ROI.
            padding: The padding around the center for the ROI.

        Returns:
            The cropped ROI.
        """
        y_min = int(max(0, y_center - padding))
        y_max = int(min(image.shape[0], y_center + padding))
        x_min = int(max(0, x_center - padding))
        x_max = int(min(image.shape[1], x_center + padding))

        return image[y_min:y_max, x_min:x_max]

    @staticmethod
    def split_blobs_with_erosion(
        image: np.ndarray, max_kernel_size: int = 50
    ) -> list[np.ndarray]:
        """Applies erosion and finds contours to attempt splitting blobs.

        Args:
            image: The input image.
            max_kernel_size: The maximum kernel size for erosion.

        Returns:
            A list of contours if found, otherwise an empty list.
        """
        copy_image = image.copy()
        for x_coords in range(1, max_kernel_size + 1):
            for y_coords in range(1, max_kernel_size + 1):
                erode_kernel = np.ones((x_coords, y_coords), np.uint8)
                eroded = cv2.erode(copy_image, erode_kernel)
                new_contours, _ = cv2.findContours(
                    eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
                )

                if not new_contours:
                    break
                if len(new_contours) > 1:
                    return new_contours
        return []
