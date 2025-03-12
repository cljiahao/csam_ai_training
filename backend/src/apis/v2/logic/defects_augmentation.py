import cv2
import random
import numpy as np
from pathlib import Path

from apis.v2.helpers.image_process_utils import (
    create_focus_chip_mask,
    extract_hsv_mask_and_area_sum,
    get_largest_info_and_mask,
)
from apis.v2.helpers.processor.train_processor import TrainProcessor
from apis.v2.helpers.processor.base_processor import BaseProcessor
from constants.tf_model import ClassLabel
from constants.image_thresholds import AugmentThreshold
from constants.colors import CSAMcolor
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager
from utils.debug import timer
from utils.image_process.image_manager import ImageManager


@timer("Defects Augmentation")
def defects_augmentation(item: str):
    """Augments defects images by applying transformations based on predefined color masks."""

    train_processor = TrainProcessor(item)
    train_processor.create_directories()

    base_processor = BaseProcessor(item)
    ng_file_paths = dm.list_png_paths(base_processor.ng_dir)
    g_file_paths = dm.list_png_paths(base_processor.g_dir)
    others_file_paths = dm.list_png_paths(base_processor.others_dir)

    augment_multiplier = len(CSAMcolor) * AugmentThreshold.BASE_MULTIPLIER.value

    base_file_paths, norm_g_file_paths = random_select_base_and_g_files(
        ng_file_paths, g_file_paths, others_file_paths, augment_multiplier
    )

    for i, ng_file_path in enumerate(ng_file_paths):

        ng_image, major_ng_mask = get_mask_from_read_image(ng_file_path)
        major_ng_roi = cv2.bitwise_and(ng_image, ng_image, mask=major_ng_mask)
        defect_mask, _ = extract_hsv_mask_and_area_sum(major_ng_roi)

        base_paths_chunk = base_file_paths[
            augment_multiplier * i : augment_multiplier * (i + 1)
        ]

        counter = 0
        for csam_color in CSAMcolor:
            for _ in range(AugmentThreshold.BASE_MULTIPLIER.value):
                base_image_path = base_paths_chunk[counter]

                base_image, major_base_mask = get_mask_from_read_image(base_image_path)
                impose_defect_mask = cv2.bitwise_and(major_base_mask, defect_mask)

                base_image[impose_defect_mask > 0] = csam_color.value.bgr

                file_name = base_image_path.name
                ImageManager.save_image(
                    train_processor.train_dir / ClassLabel.NG.value / file_name,
                    base_image,
                )

                counter += 1

    FileManager.copy_files_to_dir(
        train_processor.train_dir / ClassLabel.G.value, norm_g_file_paths, False
    )

    train_processor.train_val_split([ClassLabel.NG.value, ClassLabel.G.value])


@timer("Select Base and G Files")
def random_select_base_and_g_files(
    ng_file_paths: list[Path],
    g_file_paths: list[Path],
    others_file_paths: list[Path],
    augment_multiplier: int,
) -> tuple[list[Path], list[Path]]:

    ng_count, g_count, others_count = (
        len(ng_file_paths),
        len(g_file_paths),
        len(others_file_paths),
    )

    base_count = augment_multiplier * ng_count

    if g_count < base_count:
        raise ValueError("Not enough G images for augmentation")

    norm_g_count = (
        int(random.randrange(900, 1100) / 1000 * base_count)
        if base_count * 1.1 < g_count
        else g_count
    )

    if base_count < others_count:
        base_file_paths = random.sample(others_file_paths, base_count)
        norm_g_file_paths = random.sample(g_file_paths, norm_g_count)
        return base_file_paths, norm_g_file_paths

    remainder = base_count - others_count

    if g_count < remainder:
        raise ValueError("Not enough Base images for augmentation")

    if g_count - remainder < base_count:
        raise ValueError("Not enough G images for augmentation")

    random.shuffle(g_file_paths)
    base_file_paths = others_file_paths + g_file_paths[:remainder]
    norm_g_file_paths = random.sample(g_file_paths[remainder:], norm_g_count)
    return base_file_paths, norm_g_file_paths


def get_mask_from_read_image(image_path: Path) -> np.ndarray:
    image = ImageManager.path_to_image(image_path)
    binary_image = create_focus_chip_mask(image)
    _, major_mask = get_largest_info_and_mask(binary_image)
    return image, major_mask
