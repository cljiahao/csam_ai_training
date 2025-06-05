import cv2
import random
from pathlib import Path
from sqlalchemy.orm import Session

from apis.v2.components.utils_image_process import (
    get_base_image_mask,
    get_defect_image_mask,
)
from apis.v2.constants.csam_thresholds import DefectSizeType
from apis.v2.constants.datasets_thresholds import EvaluationDatasetsThresholds
from apis.v2.schemas.csam_image import LabeledImageData
from constants.folder_names import (
    BaseSetsFolderName,
    ColorsFolderNames,
    EvaluationSetsFolderName,
    MassProFolderNames,
    ThousandsFolderNames,
)
from constants.colors import CSAMcolor
from core.directory_manager import directory_manager as dm
from db.services.eval_sets import EvalSetsService
from utils.debug import timer
from utils.image_process.image_manager import ImageManager


@timer("Augment Eval Sets")
def augment_eval_sets(
    base_image_datas: list[LabeledImageData],
    defect_image_datas: list[LabeledImageData],
) -> list[LabeledImageData]:
    """Augments evaluation sets by imposing defects on base images."""
    augment_image_datas = []
    for base_image_data in base_image_datas:
        base_image = prepare_base_image(base_image_data)
        major_base_mask = get_base_image_mask(base_image)

        defect_image_data = random.choice(defect_image_datas)
        ng_image = prepare_base_image(defect_image_data)
        defect_mask = get_defect_image_mask(ng_image)

        impose_defect_mask = cv2.bitwise_and(major_base_mask, defect_mask)
        csam_color = random.choice([c for c in CSAMcolor if c.get_name() != "Black"])
        base_image[impose_defect_mask > 0] = csam_color.get_bgr()
        base_image_data.label_mode = BaseSetsFolderName.NG
        base_image_data.defect_color = csam_color.get_name()
        base_image_data.defect_size = defect_image_data.defect_size
        augment_image_datas.append(base_image_data)

    return augment_image_datas + defect_image_datas


@timer("Populating Eval Sets (Mass Production)")
def populate_mass_production_sets(
    item: str,
    plate_no: str,
    image_data_list: list,
    defect_file_list: list[str],
    db: Session,
) -> bool:
    """Populates mass production evaluation sets."""
    evaluation_dir = dm.images_dir / EvaluationSetsFolderName.EVALUATION / item
    mass_pro_dir = evaluation_dir / EvaluationSetsFolderName.MASS_PRO
    dm.create_directory(mass_pro_dir)

    if dm.get_folder_count(mass_pro_dir) >= EvaluationDatasetsThresholds.MASS_PRO:
        return False

    create_mass_production_sets(
        mass_pro_dir / plate_no, image_data_list, defect_file_list
    )
    eval_sets_service = EvalSetsService(db)
    eval_sets_service.create_or_update_mass_pro_eval(
        item,
        plate_no,
        {"no_of_chips": len(image_data_list), "no_of_ng": len(defect_file_list)},
    )
    return True


def create_mass_production_sets(
    mass_pro_dir: Path,
    image_data_list: list[LabeledImageData],
    defect_file_list: list[str],
) -> None:
    """Creates mass production image sets, separating temporary images from those identified as defective."""
    mass_pro_temp_dir = mass_pro_dir / MassProFolderNames.TEMP
    mass_pro_ng_dir = mass_pro_dir / MassProFolderNames.NG
    dm.create_directory(mass_pro_temp_dir)
    dm.create_directory(mass_pro_ng_dir)

    for image_data in image_data_list:
        temp_file_path = mass_pro_temp_dir / image_data.file_name
        ImageManager.save_image(temp_file_path, image_data.image_data)
        if image_data.file_name in defect_file_list:
            ng_file_path = mass_pro_ng_dir / image_data.file_name
            ImageManager.save_image(ng_file_path, image_data.image_data)


@timer("Populating Eval Sets (Colors and Thousands)")
def populate_colors_thousands_sets(
    item: str,
    non_g_image_data_list: list[LabeledImageData],
    db: Session,
) -> list[LabeledImageData]:
    """Populates evaluation sets for colors and thousands categories."""
    evaluation_dir = dm.images_dir / EvaluationSetsFolderName.EVALUATION / item
    colors_dir = evaluation_dir / EvaluationSetsFolderName.COLORS
    colors_counts = create_subdirectories_and_count(colors_dir, ColorsFolderNames)

    thousands_dir = evaluation_dir / EvaluationSetsFolderName.THOUSANDS
    thousands_counts = create_subdirectories_and_count(
        thousands_dir, ThousandsFolderNames
    )

    remaining_eval_set = []
    for image_data in non_g_image_data_list:
        color = image_data.defect_color.lower()
        size = (
            DefectSizeType.SMALL
            if image_data.defect_size is None
            else image_data.defect_size.lower()
        )
        color_size = f"{color}_{size}"
        random_value = random.random()

        per_color = EvaluationDatasetsThresholds.PER_COLOR
        if colors_counts.get(color_size, 0) < per_color and random_value < 0.45:
            save_image_and_update_counts(
                colors_dir, color_size, colors_counts, image_data
            )
            continue
        thousands_small = EvaluationDatasetsThresholds.THOUSANDS_SMALL
        thousands_med_big = EvaluationDatasetsThresholds.THOUSANDS_MED_AND_BIG
        small = ThousandsFolderNames.SMALL
        size_threshold = thousands_small if size == small else thousands_med_big
        if thousands_counts.get(size, 0) < size_threshold and random_value < 0.9:
            save_image_and_update_counts(
                thousands_dir, size, thousands_counts, image_data
            )
            continue
        remaining_eval_set.append(image_data)

    eval_sets_service = EvalSetsService(db)
    eval_sets_service.create_or_update_colors_eval(item, colors_counts)
    eval_sets_service.create_or_update_thousands_eval(item, thousands_counts)

    return remaining_eval_set


def prepare_base_image(base_image_data: LabeledImageData) -> cv2.Mat:
    """Ensures the base image is writeable and returns a copy if necessary."""
    if not base_image_data.image_data.flags.writeable:
        base_image_data.image_data = base_image_data.image_data.copy()
    return base_image_data.image_data


def create_subdirectories_and_count(
    evaluation_subdir: Path, sub_directories: list[str]
) -> dict[str, int]:
    """Creates subdirectories and counts existing files within them."""
    dm.create_subdirectories(evaluation_subdir, sub_directories)
    return dm.count_files_in_subdirectories(evaluation_subdir, sub_directories)


def save_image_and_update_counts(
    directory: Path,
    key: str,
    counts: dict[str, int],
    image_data: LabeledImageData,
) -> None:
    """Saves an image and updates the corresponding count."""
    image_path = directory / key / image_data.file_name
    ImageManager.save_image(image_path, image_data.image_data)
    counts[key] = counts.get(key, 0) + 1
