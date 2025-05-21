import cv2
import random
from itertools import product
from pathlib import Path


from apis.v2.components.utils_image_process import (
    get_base_image_mask,
    get_defect_image_mask,
)
from apis.v2.constants.csam_thresholds import AugmentThresholdRatio
from constants.folder_names import BaseSetsFolderName, ModelDatasetFolderNames
from constants.colors import CSAMcolor
from constants.tensorflow_model import DatasetModes
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager
from utils.ai_model.tensorflow_model import TensorflowModel
from utils.debug import timer
from utils.image_process.image_manager import ImageManager


def augment_base_with_defects(item: str) -> None:
    """Augments base images with defects and prepares them for training."""
    base_set_dir = dm.images_dir / BaseSetsFolderName.BASE / item
    total_ng_count, train_g_count, others_count = get_base_folder_counts(base_set_dir)
    base_file_paths, train_g_paths, ng_file_paths, deform_file_paths = (
        prepare_training_file_paths(
            total_ng_count, train_g_count, others_count, base_set_dir
        )
    )

    dataset_dir = dm.images_dir / ModelDatasetFolderNames.DATASET / item
    train_dir = dataset_dir / ModelDatasetFolderNames.TRAIN
    dm.create_subdirectories(train_dir, DatasetModes, True)

    base_path_iter = iter(base_file_paths)
    color_augmentation_steps = product(
        CSAMcolor, range(AugmentThresholdRatio.BASE_MULTIPLIER)
    )
    for ng_file_path in ng_file_paths:
        ng_image = ImageManager.path_to_image(ng_file_path)
        defect_mask = get_defect_image_mask(ng_image)

        for csam_color, _ in color_augmentation_steps:
            base_image_path = next(base_path_iter)
            base_image = ImageManager.path_to_image(base_image_path)
            major_base_mask = get_base_image_mask(base_image)

            impose_defect_mask = cv2.bitwise_and(major_base_mask, defect_mask)
            base_image[impose_defect_mask > 0] = csam_color.get_bgr()
            ImageManager.save_image(
                train_dir / DatasetModes.NG / base_image_path.name,
                base_image,
            )

    FileManager.copy_files_to_dir(train_dir / DatasetModes.NG, ng_file_paths)
    FileManager.copy_files_to_dir(train_dir / DatasetModes.NG, deform_file_paths)
    FileManager.copy_files_to_dir(train_dir / DatasetModes.GOOD, train_g_paths)

    TensorflowModel.train_validation_split(dataset_dir)


@timer("Get Base Folder Count")
def get_base_folder_counts(base_set_dir: Path) -> tuple[int, int, int]:
    """Retrieves and calculates base folder counts for augmentation."""
    base_sets_counts = dm.count_files_in_subdirectories(
        base_set_dir,
        [item for item in BaseSetsFolderName if item != BaseSetsFolderName.BASE],
    )
    ng_count = base_sets_counts.get(BaseSetsFolderName.NG, 0)
    g_count = base_sets_counts.get(BaseSetsFolderName.GOOD, 0)
    others_count = base_sets_counts.get(BaseSetsFolderName.OTHERS, 0)
    deform_count = base_sets_counts.get(BaseSetsFolderName.DEFORM, 0)

    augment_multiplier = len(CSAMcolor) * AugmentThresholdRatio.BASE_MULTIPLIER
    total_ng_count = (augment_multiplier + 1) * ng_count + deform_count

    if g_count < total_ng_count:
        raise ValueError("Not enough G images for augmentation")
    if g_count + others_count < 2 * total_ng_count:
        raise ValueError("Not Enough G or Others image for augmentation")

    train_g_count = (
        int(random.randrange(900, 1100) / 1000 * total_ng_count)
        if total_ng_count * 1.1 < g_count
        else g_count
    )

    return total_ng_count, train_g_count, others_count


@timer("Prepare training files")
def prepare_training_file_paths(
    total_ng_count: int, train_g_count: int, others_count: int, base_set_dir: Path
) -> tuple[list[Path], list[Path], list[Path], list[Path]]:
    """Prepares file paths for training, handling image selection."""
    ng_file_paths = dm.list_png_paths(base_set_dir / BaseSetsFolderName.NG)
    g_file_paths = dm.list_png_paths(base_set_dir / BaseSetsFolderName.GOOD)
    others_file_paths = dm.list_png_paths(base_set_dir / BaseSetsFolderName.OTHERS)
    deform_file_paths = dm.list_png_paths(base_set_dir / BaseSetsFolderName.DEFORM)

    if total_ng_count < others_count:
        base_file_paths = random.sample(others_file_paths, total_ng_count)
        train_g_paths = random.sample(g_file_paths, train_g_count)
    else:
        remainder = total_ng_count - others_count
        random.shuffle(g_file_paths)
        base_file_paths = random.sample(
            others_file_paths + g_file_paths[:remainder], total_ng_count
        )
        train_g_paths = random.sample(g_file_paths[remainder:], train_g_count)

    return base_file_paths, train_g_paths, ng_file_paths, deform_file_paths
