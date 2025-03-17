import random
import cv2
from apis.v2.helpers.image_process_utils import (
    create_focus_chip_mask,
    extract_hsv_mask_and_area_sum,
    get_largest_info_and_mask,
)
from constants.colors import CSAMcolor
from schemas.chips_data import ImageData
from utils.debug import timer


@timer("Augment NG images onto base images")
def augment_ng_for_eval(
    defect_imdata_list: list[ImageData],
    temp_imdata_list: list[ImageData],
) -> tuple[list[ImageData], list[ImageData]]:
    """Augments images by imposing defects from the defect images onto the temporary images."""

    # Calculate how many images to augment
    to_augment_count = len(defect_imdata_list) * random.randint(1, len(CSAMcolor))
    images_to_augment = temp_imdata_list[:to_augment_count]
    leftover_imdata_list = temp_imdata_list[to_augment_count:]

    # Augment each image by applying defects
    for base_image_data in images_to_augment:
        base_image = _prepare_base_image(base_image_data)

        # Choose a random defect and apply it to the base image
        defect_image_data = random.choice(defect_imdata_list)
        _apply_defect_to_image(base_image, defect_image_data)

        # Store defect-related metadata
        base_image_data.defect_color = defect_image_data.defect_color
        base_image_data.defect_size = defect_image_data.defect_size

    return images_to_augment + defect_imdata_list, leftover_imdata_list


def _prepare_base_image(base_image_data: ImageData) -> cv2.Mat:
    """Ensures the base image is writeable and returns a copy if necessary."""
    if not base_image_data.rotated_image.flags.writeable:
        base_image = base_image_data.rotated_image.copy()
        base_image_data.rotated_image = base_image
    else:
        base_image = base_image_data.rotated_image
    return base_image


def _apply_defect_to_image(base_image: cv2.Mat, defect_image_data: ImageData) -> None:
    """Applies a random defect onto the base image."""
    defect_image = defect_image_data.rotated_image

    # Generate the defect mask
    defect_bin_image = create_focus_chip_mask(defect_image)
    _, largest_defect_mask = get_largest_info_and_mask(defect_bin_image)

    major_defect_roi = cv2.bitwise_and(
        defect_image, defect_image, mask=largest_defect_mask
    )
    defect_mask, _ = extract_hsv_mask_and_area_sum(major_defect_roi)

    # Generate the base image mask
    base_bin_image = create_focus_chip_mask(base_image)
    _, largest_base_mask = get_largest_info_and_mask(base_bin_image)

    # Combine the base image with the defect mask
    impose_defect_mask = cv2.bitwise_and(
        largest_base_mask, largest_base_mask, mask=defect_mask
    )
    csam_color = random.choice([c.value for c in CSAMcolor])

    base_image[impose_defect_mask > 0] = csam_color.bgr
