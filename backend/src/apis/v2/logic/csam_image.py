import random
import numpy as np
from typing import Callable
from pathlib import Path
from sqlalchemy.orm import Session

from apis.v2.components.create_evaluation_sets import (
    augment_eval_sets,
    populate_colors_thousands_sets,
    populate_mass_production_sets,
)
from apis.v2.components.create_training_sets import (
    populate_base_folders,
    populate_retrain_folders,
)
from apis.v2.components.defects_classification import (
    classify_black_defect_mode,
    classify_non_black_defect_mode,
)
from apis.v2.components.utils_image_process import convert_white_bg_to_gray_to_binary
from apis.v2.components.process_chips import (
    create_chip_contour_info_list,
    rotate_and_crop_chip_image,
)
from apis.v2.constants.csam_thresholds import AugmentThresholdRatio
from apis.v2.schemas.common import ChipThreshold
from apis.v2.schemas.csam_image import DefectInfo, LabeledImageData
from constants.folder_names import BaseSetsFolderName, ReTrainFolderName
from db.models.image_settings import ImageSettings
from db.services.image_settings import ImageSettingsService
from schemas.contours import ContourInfo, ContourInfoList
from utils.debug import timer
from utils.image_process.border_creator import BorderCreator
from utils.image_process.image_manager import ImageManager
from utils.misc.calculations import calculate_border_padding


@timer("Preparing Datasets for Training Model")
def prepare_datasets_for_training(
    item: str,
    lot_no: str,
    file_name: str,
    file_path: str,
    defect_file_list: list[str],
    db: Session,
) -> None:
    """Prepares datasets for model training by processing a CSAM image and organizing chips."""
    plate_no = Path(file_name).stem
    image = ImageManager.path_to_image(file_path)
    image_datas = process_csam_image(item, lot_no, plate_no, image, db)

    if populate_mass_production_sets(item, plate_no, image_datas, defect_file_list, db):
        return

    defect_image_datas = [
        image_data
        for image_data in image_datas
        if image_data.file_name in defect_file_list
    ]
    ng_image_datas = filter_by_label_mode(image_datas, BaseSetsFolderName.NG)
    others_image_datas = filter_by_label_mode(image_datas, BaseSetsFolderName.OTHERS)
    all_defect_image_datas = defect_image_datas + ng_image_datas

    base_multiplier = AugmentThresholdRatio.BASE_MULTIPLIER
    to_augment_image_limit = base_multiplier * len(all_defect_image_datas)
    images_to_augment = others_image_datas[:to_augment_image_limit]

    augment_image_datas = augment_eval_sets(images_to_augment, all_defect_image_datas)
    remainder_ng_images = populate_colors_thousands_sets(item, augment_image_datas, db)
    if remainder_ng_images:
        base_image_datas = {
            BaseSetsFolderName.NG: remainder_ng_images,
            BaseSetsFolderName.GOOD: filter_by_label_mode(
                image_datas, BaseSetsFolderName.GOOD
            ),
            BaseSetsFolderName.OTHERS: others_image_datas[to_augment_image_limit:],
            BaseSetsFolderName.DEFORM: filter_by_label_mode(
                image_datas, BaseSetsFolderName.DEFORM
            ),
        }
        populate_base_folders(item, base_image_datas, db)


@timer("Preparing Datasets for Re-training Model")
def prepare_datasets_for_retraining(
    item: str,
    lot_no: str,
    file_name: str,
    file_path: str,
    defect_file_list: list[str],
    db: Session,
) -> None:
    """Prepares datasets for model training by processing a CSAM image and organizing chips."""
    plate_no = Path(file_name).stem
    image = ImageManager.path_to_image(file_path)
    image_datas = process_csam_image(item, lot_no, plate_no, image, db)

    defect_image_datas = [
        image_data
        for image_data in image_datas
        if image_data.file_name in defect_file_list
    ]
    good_image_datas = filter_by_label_mode(image_datas, BaseSetsFolderName.GOOD)
    others_image_datas = filter_by_label_mode(image_datas, BaseSetsFolderName.OTHERS)
    random_good_image_datas = random.sample(good_image_datas, 100)
    random_others_image_datas = random.sample(others_image_datas, 5)
    non_defect_image_datas = random_good_image_datas + random_others_image_datas

    retrain_image_datas = {
        ReTrainFolderName.NG: defect_image_datas,
        ReTrainFolderName.GOOD: non_defect_image_datas,
    }
    populate_retrain_folders(item, retrain_image_datas, db)


def filter_by_label_mode(
    image_datas: list[LabeledImageData], label_mode: str
) -> list[LabeledImageData]:
    """Filters a list of LabeledImageData objects by label_mode"""
    return [
        image_data for image_data in image_datas if image_data.label_mode == label_mode
    ]


@timer("Processing CSAM Image")
def process_csam_image(
    item: str, lot_no: str, plate_no: str, image: np.ndarray, db: Session
) -> list[LabeledImageData]:
    """Processes a single CSAM image to identify and classify chips."""
    image_settings = get_or_fetch_image_settings(item, db)
    crop_size = image_settings.crop_size

    border_padding = calculate_border_padding(crop_size)
    border_image = BorderCreator.create_border_image(image, border_padding)
    binary_image = convert_white_bg_to_gray_to_binary(border_image)
    base_file_name = f"{lot_no}_{plate_no}"

    black_refined_contour_infos, non_black_refined_contour_infos, chip_threshold = (
        create_chip_contour_info_list(border_image, binary_image, image_settings)
    )

    combined_contour_infos = [
        (black_refined_contour_infos, classify_black_defect_mode),
        (non_black_refined_contour_infos, classify_non_black_defect_mode),
    ]
    combined_image_data_list = []
    for contour_infos, classify_function in combined_contour_infos:
        image_data_list = rotate_and_classify_contours(
            contour_infos,
            len(combined_image_data_list),
            border_image,
            border_padding,
            crop_size,
            classify_function,
            chip_threshold,
            base_file_name,
        )
        combined_image_data_list.extend(image_data_list)

    return combined_image_data_list


@timer("Get Image Settings")
def get_or_fetch_image_settings(item: str, db: Session) -> ImageSettings:
    image_settings_service = ImageSettingsService(db)
    return image_settings_service.read_image_settings_not_empty(item)


def rotate_and_classify_contours(
    contour_infos: ContourInfoList,
    prev_count: int,
    image: np.ndarray,
    padding: int,
    crop_size: int,
    classify_function: Callable[[ChipThreshold, ContourInfo, np.ndarray], DefectInfo],
    chip_threshold: ChipThreshold,
    base_file_name: str,
) -> list[LabeledImageData]:
    image_data_list = []
    for i, contour_info in enumerate(contour_infos, start=prev_count + 1):
        rotated_image = rotate_and_crop_chip_image(
            contour_info, image, padding, crop_size
        )
        defect_info = classify_function(chip_threshold, contour_info, rotated_image)
        label_image_data = LabeledImageData(
            file_name=f"{base_file_name}_{i}.png",
            image_data=rotated_image,
            **defect_info.model_dump(),
        )
        image_data_list.append(label_image_data)
    return image_data_list
