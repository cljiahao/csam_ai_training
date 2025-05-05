import math
import random
from collections import defaultdict
from pathlib import Path
from sqlalchemy.orm import Session

from apis.v2.constants.csam_thresholds import AugmentThresholdRatio
from apis.v2.constants.datasets_thresholds import DatasetSummaryThresholds
from apis.v2.schemas.csam_image import LabeledImageData
from constants.colors import CSAMcolor
from constants.folder_names import BaseSetsFolderName
from core.directory_manager import directory_manager as dm
from core.logging import logger
from db.services.base_sets import BaseSetsService
from utils.debug import timer
from utils.image_process.image_manager import ImageManager


@timer("Populating Base Folders")
def populate_base_folders(
    item: str, image_data_list: list[LabeledImageData], db: Session
) -> None:
    """Populates base folders with images based on labels."""
    label_image_dict = group_image_data_by_label(image_data_list)
    base_dir = setup_base_sets_environment(item, label_image_dict)
    label_folder_counts = dm.count_files_in_subdirectories(
        base_dir, label_image_dict.keys()
    )

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


def group_image_data_by_label(
    image_data_list: list[LabeledImageData],
) -> dict[str, list[LabeledImageData]]:
    """Groups a list of LabeledImageData objects by their label mode."""
    label_image_dict = defaultdict(list[LabeledImageData])
    for image_data in image_data_list:
        label_image_dict[image_data.label_mode].append(image_data)
    return label_image_dict


def setup_base_sets_environment(
    item: str, label_image_dict: dict[str, list[LabeledImageData]]
) -> Path:
    """Sets up the base sets directory environment."""
    base_dir = dm.images_dir / BaseSetsFolderName.BASE / item
    dm.create_subdirectories(base_dir, label_image_dict.keys())
    return base_dir
