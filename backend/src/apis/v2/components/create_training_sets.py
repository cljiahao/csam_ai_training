import math
import random
from collections import defaultdict
from pathlib import Path
from sqlalchemy.orm import Session

from apis.v2.constants.csam_thresholds import AugmentThresholdRatio
from apis.v2.constants.datasets_thresholds import DatasetSummaryThresholds
from apis.v2.schemas.csam_image import LabeledImageData
from constants.colors import CSAMcolor
from constants.folder_names import BaseSetsFolderName, ReTrainFolderName
from core.directory_manager import directory_manager as dm
from core.logging import logger
from db.services.base_sets import BaseSetsService
from db.services.retrain_sets import ReTrainSetsService
from utils.debug import timer
from utils.image_process.image_manager import ImageManager


@timer("Populating Base Folders")
def populate_base_folders(
    item: str, label_image_dict: dict[str, list[LabeledImageData]], db: Session
) -> None:
    """Populates base folders with images based on labels."""
    base_dir = setup_folder_environment(BaseSetsFolderName.BASE, item, label_image_dict)
    labels = label_image_dict.keys()
    label_folder_counts = dm.count_files_in_subdirectories(base_dir, labels)

    for label, image_data_list in label_image_dict.items():
        max_file_count = DatasetSummaryThresholds.MAX_DATASET
        if label == BaseSetsFolderName.NG:
            augment_multiplier = len(CSAMcolor) * AugmentThresholdRatio.BASE_MULTIPLIER
            max_file_count = math.floor(max_file_count / augment_multiplier)

        required_count = max_file_count - label_folder_counts[label]
        if required_count == 0:
            logger.info(
                f"Label: {label} already has the required {max_file_count} files."
            )
            continue

        if required_count < len(image_data_list):
            random.shuffle(image_data_list)

        images_to_save = image_data_list[:required_count]
        for image_data in images_to_save:
            ImageManager.save_image(
                base_dir / label / image_data.file_name, image_data.image_data
            )
        label_folder_counts[label] += len(images_to_save)
        logger.info(f"label: {label} has {label_folder_counts[label]} files.")

    base_sets_service = BaseSetsService(db)
    base_sets_service.create_or_update_base_sets(item, label_folder_counts)


@timer("Populating Re-Train Folders")
def populate_retrain_folders(
    item: str, label_image_dict: dict[str, list[LabeledImageData]], db: Session
) -> None:
    """Populates re-train folders with images based on labels."""
    base_dir = setup_folder_environment(
        ReTrainFolderName.RETRAIN, item, label_image_dict
    )
    labels = label_image_dict.keys()
    label_folder_counts = dm.count_files_in_subdirectories(base_dir, labels)

    for label, image_data_list in label_image_dict.items():
        max_file_count = DatasetSummaryThresholds.MAX_DATASET
        required_count = max_file_count - label_folder_counts[label]
        if required_count == 0:
            logger.info(
                f"Label: {label} already has the required {max_file_count} files."
            )
            continue

        if required_count < len(image_data_list):
            random.shuffle(image_data_list)

        images_to_save = image_data_list[:required_count]
        for image_data in images_to_save:
            ImageManager.save_image(
                base_dir / label / image_data.file_name, image_data.image_data
            )
        label_folder_counts[label] += len(images_to_save)
        logger.info(f"label: {label} has {label_folder_counts[label]} files.")

    retrain_sets_service = ReTrainSetsService(db)
    retrain_sets_service.create_or_update_retrain_sets(item, label_folder_counts)


def setup_folder_environment(
    base_folder: str, item: str, label_image_dict: dict[str, list[LabeledImageData]]
) -> Path:
    """Sets up the training sets directory environment."""
    train_dir = dm.images_dir / base_folder / item
    dm.create_subdirectories(train_dir, label_image_dict.keys())
    return train_dir
