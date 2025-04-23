import random
from pathlib import Path
from fastapi import UploadFile
from sqlalchemy.orm import Session
from collections import defaultdict

from apis.v2.components.defects_data_process import process_chunk_contours
from apis.v2.components.evaluation_sets import create_evaluation_sets
from apis.v2.components.image_process import pre_process_image
from apis.v2.schemas.files import FileDataBatchDirectory
from constants.folder_names import FolderNames
from constants.image_thresholds import AugmentThreshold
from constants.tf_model import ClassLabel
from core.directory_manager import directory_manager as dm
from core.logging import logger
from db.services.base_sets import BaseSetsService
from schemas.chips_data import ImageData
from utils.debug import timer
from utils.image_process.image_manager import ImageManager


@timer("Extract eval and base sets from image")
def eval_base_image_sets_creation(
    item: str,
    lot_no: str,
    file: UploadFile,
    defect_batch_directory: FileDataBatchDirectory,
    db: Session,
) -> None:
    """Main function to process base image creation."""

    plate_no = Path(file.filename).stem
    image_data_list = process_csam_image(file, item, lot_no, plate_no, db)

    ng_data_file_names = [
        data_file.file_name
        for defect_batch in defect_batch_directory.file_data_batches
        for data_file in defect_batch.data_files
        if data_file.defect_mode.lower() != "temp"
    ]

    leftover_imdata_list = create_evaluation_sets(
        item, plate_no, image_data_list, ng_data_file_names, db
    )

    if not leftover_imdata_list:
        return

    label_image_data = defaultdict(list[ImageData])
    for image_data in leftover_imdata_list:
        label_image_data[image_data.label_mode].append(image_data)

    base_dir = dm.images_dir / FolderNames.BASE.value / item

    for class_label in ClassLabel:
        if class_label.value == ClassLabel.TEMP.value:
            continue
        dm.create_directory(base_dir / class_label.value)

    base_fol_count = {
        base_folder.name: len(list(base_folder.iterdir()))
        for base_folder in base_dir.iterdir()
    }

    for label, image_data_list in label_image_data.items():
        required_count = AugmentThreshold.MAX_FILE_COUNT.value - base_fol_count[label]
        if required_count != 0:
            random.shuffle(image_data_list)
            logger.info(f"label: {label} has {len(image_data_list)}")
            for image_data in image_data_list[:required_count]:
                ImageManager.save_image(
                    base_dir / label / image_data.file_name, image_data.rotated_image
                )
                base_fol_count[label] += 1

    base_sets_service = BaseSetsService(db)
    base_sets_service.create_or_update_base_sets(item, base_fol_count)


@timer("Process CSAM Image")
def process_csam_image(
    file: UploadFile, item: str, lot_no: str, plate_no: str, db: Session
) -> list[ImageData]:
    """Processes the CSAM image, including contour extraction and defect processing."""
    image = ImageManager.file_to_image(file)

    (
        defect_processor,
        base_file_name,
        refined_contours_info_list,
        border_image,
    ) = pre_process_image(image, item, lot_no, plate_no, db)

    return process_chunk_contours(
        defect_processor,
        base_file_name,
        refined_contours_info_list,
        border_image,
    )
