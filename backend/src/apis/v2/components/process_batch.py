import cv2
import numpy as np

from apis.v2.schemas.image_settings import BatchCoordinates
from schemas.contours import ContourInfoList
from utils.image_process.blob_handler import BlobHandler
from utils.image_process.contour_handler import ContourHandler


def apply_morphology_for_batch(
    mask_image: np.ndarray, batch_erode: int, batch_close: int
) -> np.ndarray:
    """Applies morphological operations to the binary mask."""
    erode_kernel = BlobHandler.create_kernel(batch_erode)
    eroded_image = cv2.erode(mask_image, erode_kernel)

    close_kernel = BlobHandler.create_kernel(batch_close)
    closed_image = cv2.morphologyEx(eroded_image, cv2.MORPH_CLOSE, close_kernel)

    return closed_image


def batch_contours_clean(
    contour_info_list: ContourInfoList,
) -> ContourInfoList:
    """Filters a list of contours to keep those with sizes close to the median."""
    avg_contour_area = contour_info_list.get_median_area()
    same_size_contours = [
        contour_info
        for contour_info in contour_info_list
        if avg_contour_area * 0.9 < contour_info.area
    ]
    return ContourInfoList(contours=same_size_contours)


def create_batch_coordinates(
    contour_info_list: ContourInfoList, binary_image: np.ndarray
) -> list[BatchCoordinates]:
    """Creates a list of normalized coordinates and dimensions for each contour."""
    norm_coordinates_list = ContourHandler.extract_norm_coordinates(
        contour_info_list, binary_image.shape[:2]
    )

    norm_dimensions_list = ContourHandler.extract_norm_coordinates(
        contour_info_list, binary_image.shape[:2], rect_index=1
    )

    return [
        BatchCoordinates(
            norm_x_center=norm_coords.norm_x,
            norm_y_center=norm_coords.norm_y,
            norm_batch_width=norm_dims.norm_x,
            norm_batch_height=norm_dims.norm_y,
        )
        for norm_coords, norm_dims in zip(norm_coordinates_list, norm_dimensions_list)
    ]
