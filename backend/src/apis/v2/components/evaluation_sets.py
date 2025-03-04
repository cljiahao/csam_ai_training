import random

import cv2
from apis.v2.components.extract_roi import (
    create_focus_chip_mask,
    get_hsv_mask_and_contour_area,
    get_largest_info_and_mask,
)
from constants.colors import CSAMcolor
from schemas.chips_data import ImageData


def augment_ng_for_eval(
    defect_imdata_list: list[ImageData],
    base_imdata_list: list[ImageData],
) -> list[ImageData]:

    for base_image_data in base_imdata_list:

        if not base_image_data.rotated_image.flags.writeable:
            base_image = base_image_data.rotated_image.copy()
            base_image_data.rotated_image = base_image

        bin_image = create_focus_chip_mask(base_image)
        _, largest_base_mask = get_largest_info_and_mask(bin_image)

        defect_image_data = random.choice(defect_imdata_list)
        defect_image = defect_image_data.rotated_image
        defect_bin_image = create_focus_chip_mask(defect_image)
        _, largest_defect_mask = get_largest_info_and_mask(defect_bin_image)

        major_defect_roi = cv2.bitwise_and(
            defect_image, defect_image, mask=largest_defect_mask
        )
        defect_mask, _ = get_hsv_mask_and_contour_area(major_defect_roi)
        impose_defect_mask = cv2.bitwise_and(largest_base_mask, defect_mask)
        csam_color = random.choice([c.value for c in CSAMcolor])

        base_image[impose_defect_mask > 0] = csam_color.bgr

        base_image_data.defect_color = csam_color.name
        base_image_data.defect_size = defect_image_data.defect_size

    return base_imdata_list + defect_imdata_list
