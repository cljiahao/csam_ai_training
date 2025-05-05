import cv2
import numpy as np
from pathlib import Path
from sqlalchemy.orm import Session

from apis.v2.components.create_base_sets import populate_base_folders
from apis.v2.components.create_evaluation_sets import (
    augment_eval_sets,
    populate_colors_thousands_sets,
    populate_mass_production_sets,
)
from apis.v2.components.defects_classification import (
    classify_black_defect_mode,
    classify_non_black_defect_mode,
)
from apis.v2.components.utils_image_process import create_contour_list
from apis.v2.components.process_chips import (
    apply_morphology_for_chips,
    create_black_chip_mask,
    extract_refined_contour_info_list,
    rotate_and_crop_chip_image,
    update_chip_threshold,
)
from apis.v2.constants.csam_thresholds import AugmentThresholdRatio, CSAMThresholdRatio
from apis.v2.schemas.csam_image import LabeledImageData
from constants.folder_names import BaseSetsFolderName
from db.models.image_settings import ImageSettings
from db.services.image_settings import ImageSettingsService
from schemas.contours import ContourInfoList
from utils.debug import timer
from utils.image_process.border_creator import BorderCreator
from utils.image_process.image_manager import ImageManager
from utils.misc.calculations import calculate_border_padding


@timer("Preparing Datasets for Model")
def prepare_datasets_for_model(
    item: str,
    lot_no: str,
    file_name: str,
    file_path: str,
    defect_file_list: list[str],
    db: Session,
) -> None:
    """Prepares datasets for model training by processing a CSAM image and organizing chips."""
    plate_no = Path(file_name).stem
    image_datas = process_csam_image(item, lot_no, plate_no, file_path, db)

    if populate_mass_production_sets(item, plate_no, image_datas, defect_file_list, db):
        return

    defect_image_datas = [
        image_data
        for image_data in image_datas
        if image_data.file_name in defect_file_list
        or image_data.label_mode == BaseSetsFolderName.NG
    ]

    remnant_others_image_datas = [
        image_data
        for image_data in image_datas
        if image_data.label_mode == BaseSetsFolderName.OTHERS
    ]

    base_multiplier = AugmentThresholdRatio.BASE_MULTIPLIER
    to_augment_image_limit = base_multiplier * len(defect_image_datas)
    to_augment_image_datas = remnant_others_image_datas[:to_augment_image_limit]

    augment_image_datas = augment_eval_sets(to_augment_image_datas, defect_image_datas)
    remnant_augment_image_datas = populate_colors_thousands_sets(
        item, augment_image_datas, db
    )
    if remnant_augment_image_datas:
        good_image_datas = [
            image_data
            for image_data in image_datas
            if image_data.label_mode == BaseSetsFolderName.G
        ]
        remnant_others_image_datas = remnant_others_image_datas[to_augment_image_limit:]
        base_image_datas = (
            good_image_datas + remnant_others_image_datas + remnant_augment_image_datas
        )
        populate_base_folders(item, base_image_datas, db)


@timer("Processing CSAM Image")
def process_csam_image(
    item: str, lot_no: str, plate_no: str, file_path: str, db: Session
) -> list[LabeledImageData]:
    """Processes a single CSAM image to identify and classify chips."""
    image_settings_service = ImageSettingsService(db)
    image_settings = image_settings_service.read_image_settings_not_empty(item)
    crop_size = image_settings.crop_size

    image = ImageManager.path_to_image(file_path)
    border_padding = calculate_border_padding(crop_size)
    border_image = BorderCreator.create_border_image(image, border_padding)
    base_file_name = f"{lot_no}_{plate_no}"

    black_contour_info_list = find_black_contours(border_image)
    non_black_contour_info_list = find_non_black_contours(border_image, image_settings)

    chip_threshold = update_chip_threshold(non_black_contour_info_list)

    black_refined_contour_infos = extract_refined_contour_info_list(
        black_contour_info_list, border_image, crop_size, chip_threshold
    )
    non_black_refined_contour_infos = extract_refined_contour_info_list(
        non_black_contour_info_list, border_image, crop_size, chip_threshold
    )

    image_data_list = []
    for i, contour_info in enumerate(black_refined_contour_infos, start=1):
        rotated_image = rotate_and_crop_chip_image(
            contour_info, border_image, border_padding, crop_size
        )
        defect_info = classify_black_defect_mode(rotated_image)
        label_image_data = LabeledImageData(
            file_name=f"{base_file_name}_{i}.png",
            image_data=rotated_image,
            **defect_info.model_dump(),
        )
        image_data_list.append(label_image_data)

    black_count = len(image_data_list)
    for j, contour_info in enumerate(
        non_black_refined_contour_infos, start=black_count + 1
    ):
        rotated_image = rotate_and_crop_chip_image(
            contour_info, border_image, border_padding, crop_size
        )
        defect_info = classify_non_black_defect_mode(
            chip_threshold, contour_info, rotated_image
        )
        label_image_data = LabeledImageData(
            file_name=f"{base_file_name}_{j}.png",
            image_data=rotated_image,
            **defect_info.model_dump(),
        )
        image_data_list.append(label_image_data)

    return image_data_list


def find_black_contours(image: np.ndarray) -> ContourInfoList:
    """Finds contours of black regions in the image."""
    black_mask_chip = create_black_chip_mask(image)
    return create_contour_list(black_mask_chip)


def find_non_black_contours(
    image: np.ndarray, image_settings: ImageSettings
) -> ContourInfoList:
    """Finds contours of non-black regions in the image."""
    border_gray = BorderCreator.convert_background_white_and_grayscale(
        image, CSAMThresholdRatio.BACKGROUND_THRESHOLD
    )
    bright_bg_threshold = CSAMThresholdRatio.BRIGHT_BACKGROUND_THRESHOLD
    _, binary_image = cv2.threshold(
        border_gray, bright_bg_threshold, 255, cv2.THRESH_BINARY_INV
    )
    non_black_mask_chip = apply_morphology_for_chips(
        binary_image,
        image_settings.chip_noise_erode,
        image_settings.chip_dilate,
        image_settings.chip_erode,
    )
    return create_contour_list(non_black_mask_chip)
