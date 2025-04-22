import random
from sqlalchemy.orm import Session

from apis.v2.components.eval_augment import augment_ng_for_eval
from apis.v2.helpers.processor.eval_processor import EvalProcessor
from constants.tf_model import ClassLabel
from core.directory_manager import directory_manager as dm
from db.services.eval_sets import EvalSetsService
from schemas.chips_data import ImageData
from utils.debug import timer
from utils.image_process.image_manager import ImageManager


@timer("Create Evaluation sets")
def create_evaluation_sets(
    item: str,
    plate_no: str,
    image_data_list: list[ImageData],
    defect_file_list: list[str],
    db: Session,
) -> list[ImageData]:

    defect_imdata_list = [
        image_data
        for image_data in image_data_list
        if image_data.file_name in defect_file_list
    ]

    eval_sets_service = EvalSetsService(db)
    eval_processor = EvalProcessor(item)
    eval_processor.create_directories()

    if eval_processor.should_save_mass_pro():

        _save_mass_pro_images(
            eval_processor, plate_no, image_data_list, defect_imdata_list
        )

        eval_sets_service.create_mass_pro_eval(
            item,
            plate_no,
            {
                "no_of_chips": len(image_data_list),
                "no_of_ng": len(defect_imdata_list),
            },
        )
        return []

    temp_imdata_list = [
        image_data
        for image_data in image_data_list
        if image_data.file_name not in defect_file_list
    ]
    random.shuffle(temp_imdata_list)

    augmented_imdata_list, leftover_imdata_list = augment_ng_for_eval(
        defect_imdata_list, temp_imdata_list
    )

    _save_augmented_images(eval_processor, augmented_imdata_list)

    eval_sets_service.create_colors_eval(item, eval_processor.colors_count)
    eval_sets_service.create_thousands_eval(item, eval_processor.thousands_count)

    return leftover_imdata_list


def _save_mass_pro_images(
    eval_processor: EvalProcessor,
    plate_no: str,
    image_data_list: list[ImageData],
    defect_imdata_list: list[ImageData],
) -> None:
    """Saves images into the Mass Production directory."""

    file_dir = eval_processor.mass_pro_dir / plate_no

    for mass_pro_name in [ClassLabel.TEMP.value, ClassLabel.NG.value]:
        dm.create_directory(file_dir / mass_pro_name)

    for image_data in image_data_list:
        ImageManager.save_image(
            file_dir / ClassLabel.TEMP.value / image_data.file_name,
            image_data.rotated_image,
        )

    for image_data in defect_imdata_list:
        ImageManager.save_image(
            file_dir / ClassLabel.NG.value / image_data.file_name,
            image_data.rotated_image,
        )


def _save_augmented_images(
    eval_processor: EvalProcessor, augmented_imdata_list: list[ImageData]
) -> list[ImageData]:
    """Saves augmented images into their respective directories (Colors or Thousands sets)."""

    for augmented_image_data in augmented_imdata_list:
        file_name = augmented_image_data.file_name
        color = augmented_image_data.defect_color.lower()
        size = augmented_image_data.defect_size.lower()
        color_size = f"{color}_{size}"

        if eval_processor.should_save_colors(color_size) and random.random() < 0.5:
            ImageManager.save_image(
                eval_processor.colors_dir / color_size / file_name,
                augmented_image_data.rotated_image,
            )
            eval_processor.increment_colors_count(color_size)
        elif eval_processor.should_save_thousands(size):
            ImageManager.save_image(
                eval_processor.thousands_dir / size / file_name,
                augmented_image_data.rotated_image,
            )
            eval_processor.increment_thousands_count(size)
