import random
from pathlib import Path
from fastapi import UploadFile
from sqlalchemy.orm import Session
from collections import defaultdict

from apis.v2.components.defects_data_process import process_chunk_contours
from apis.v2.components.image_process import process_csam_image
from apis.v2.helpers.processor.eval_processor import EvalProcessor
from apis.v2.schemas.files import FileDataBatchDirectory
from constants.folder_names import FolderNames
from constants.image_thresholds import AugmentThreshold
from constants.tf_model import ClassLabel
from core.directory import directory
from core.logging import logger
from db.services.base_sets import BaseSetsService
from schemas.chips_data import ImageData
from utils.os_handle.file_manager import FileManager
from utils.os_handle.image_manager import ImageManager


def process_image_file(
    item: str,
    lot_no: str,
    file: UploadFile,
    defect_batch_directory: FileDataBatchDirectory,
    db: Session,
) -> None:

    plate_no = Path(file.filename).stem

    image = ImageManager.file_to_image(file)

    (
        defect_processor,
        base_file_name,
        refined_contours_info_list,
        border_image,
    ) = process_csam_image(image, item, lot_no, plate_no, db)

    image_data_list = process_chunk_contours(
        defect_processor,
        base_file_name,
        refined_contours_info_list,
        border_image,
    )

    ng_data_file_names = [
        data_file.file_name
        for defect_batch in defect_batch_directory.file_data_batches
        for data_file in defect_batch.data_files
        if data_file.defect_mode == "ng"
    ]

    eval_processor = EvalProcessor(item, plate_no, image_data_list, ng_data_file_names)
    leftover_imdata_list, leftover_aug_imdata_list = (
        eval_processor.create_evaluation_set(db)
    )

    if leftover_imdata_list is None:
        return

    label_image_data = defaultdict(list[ImageData])
    for image_data in leftover_imdata_list:
        label_image_data[image_data.label_mode].append(image_data)
    label_image_data[ClassLabel.NG.value].extend(leftover_aug_imdata_list)

    base_dir = directory.images_dir / FolderNames.BASE.value / item

    for class_label in ClassLabel:
        if class_label.value == ClassLabel.TEMP.value:
            continue
        FileManager.prepare_dst_dir(base_dir / class_label.value)

    base_fol_count = {
        base_folder.name: len(list(base_folder.iterdir()))
        for base_folder in base_dir.iterdir()
    }

    for label, image_data_list in label_image_data.items():
        if AugmentThreshold.MAX_FILE_COUNT.value - base_fol_count[label] != 0:
            random.shuffle(image_data_list)
            logger.info(f"label: {label} has {len(image_data_list)}")
            for image_data in image_data_list[: base_fol_count[label]]:
                ImageManager.save_image(
                    base_dir / label / image_data.file_name, image_data.rotated_image
                )
                base_fol_count[label] += 1

    base_sets_service = BaseSetsService(db)
    base_sets_service.create_or_update_base_sets(item, base_fol_count)
