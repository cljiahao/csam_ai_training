import random
from sqlalchemy.orm import Session

from apis.v2.components.evaluation_sets import augment_ng_for_eval
from constants.colors import CSAMcolor
from constants.folder_names import FolderNames
from constants.image_thresholds import (
    EvalColorNames,
    EvalThousandNames,
    EvaluationThreshold,
)
from constants.tf_model import ClassLabel
from db.services.eval_sets import EvalSetsService
from schemas.chips_data import ImageData
from utils.os_handle.file_manager import FileManager
from utils.os_handle.image_manager import ImageManager
from core.directory_manager import directory_manager as dm


class EvalProcessor:
    def __init__(
        self,
        item: str,
        plate_no: str,
        image_data_list: list[ImageData],
        defect_file_list: list[str],
    ) -> None:
        self.item: str = item
        self.file_name: str = plate_no
        self.image_data_list: list[ImageData] = image_data_list
        self.defect_file_list: list[str] = defect_file_list
        self._initialize_directory()
        self._create_defect_and_temp_list()

    def _initialize_directory(self) -> None:
        eval_dir = dm.images_dir / FolderNames.EVAL.value / self.item
        self.mass_lot_dir = eval_dir / FolderNames.MASS_PRO.value
        self.color_dir = eval_dir / FolderNames.COLORS.value
        self.thousand_dir = eval_dir / FolderNames.THOUSAND.value

    def _create_defect_and_temp_list(self) -> None:
        self.defect_imdata_list = [
            image_data
            for image_data in self.image_data_list
            if image_data.file_name in self.defect_file_list
        ]

        self.temp_imdata_list = [
            image_data
            for image_data in self.image_data_list
            if image_data.file_name not in self.defect_file_list
        ]
        random.shuffle(self.temp_imdata_list)

    def _create_mass_pro_evaluation(self) -> None:
        file_dir = self.mass_lot_dir / self.file_name
        FileManager.prepare_dst_dir(file_dir / ClassLabel.TEMP.value, True)
        FileManager.prepare_dst_dir(file_dir / ClassLabel.NG.value, True)

        [
            ImageManager.save_image(
                file_dir / ClassLabel.TEMP.value / image_data.file_name,
                image_data.rotated_image,
            )
            for image_data in self.image_data_list
        ]
        [
            ImageManager.save_image(
                file_dir / ClassLabel.NG.value / image_data.file_name,
                image_data.rotated_image,
            )
            for image_data in self.defect_imdata_list
        ]

    def _ini_color_eval_count(self) -> dict[str, int]:
        for color_names in EvalColorNames:
            FileManager.prepare_dst_dir(self.color_dir / color_names.value)

        return {
            color_folder.name: len(list(color_folder.iterdir()))
            for color_folder in self.color_dir.iterdir()
        }

    def _ini_thousand_eval_count(self) -> dict[str, int]:
        for thousand_names in EvalThousandNames:
            FileManager.prepare_dst_dir(self.thousand_dir / thousand_names.value)

        return {
            thousand_fol.name: len(list(thousand_fol.iterdir()))
            for thousand_fol in self.thousand_dir.iterdir()
        }

    def create_evaluation_set(
        self, db: Session
    ) -> tuple[list[ImageData], list[ImageData]]:

        eval_set_service = EvalSetsService(db)

        FileManager.prepare_dst_dir(self.mass_lot_dir)
        if (
            len(list(self.mass_lot_dir.iterdir()))
            < EvaluationThreshold.MIN_MASS_PRO_SET.value
        ):
            self._create_mass_pro_evaluation()
            eval_set_service.create_mass_pro_eval(
                self.item,
                {
                    "plate_no": self.file_name,
                    "no_of_chips": len(self.temp_imdata_list),
                    "no_of_ng": len(self.defect_imdata_list),
                },
            )
            return None, None

        color_eval_count = self._ini_color_eval_count()
        thousand_eval_count = self._ini_thousand_eval_count()

        to_augment_count = len(self.defect_file_list) * random.randint(
            1, len(CSAMcolor)
        )
        to_augment_imdata_list = self.temp_imdata_list[:to_augment_count]
        leftover_imdata_list = self.temp_imdata_list[to_augment_count:]

        augmented_imdata_list = augment_ng_for_eval(
            self.defect_imdata_list, to_augment_imdata_list
        )

        leftover_aug_imdata_list = []
        for augmented_image_data in augmented_imdata_list:
            color = augmented_image_data.defect_color.lower()
            size = augmented_image_data.defect_size.lower()
            file_name = augmented_image_data.file_name
            color_size = f"{color}_{size}"

            should_save_color = (
                color_size in color_eval_count
                and color_eval_count[color_size]
                < EvaluationThreshold.MIN_PER_COLOR_SET.value
            )

            thousand_threshold = (
                EvaluationThreshold.MIN_SMALL_THOUSAND_SET.value
                if size == EvalThousandNames.SMALL.value
                else EvaluationThreshold.MIN_MEDIUM_BIG_THOUSAND_SET.value
            )

            should_save_thousand = size in thousand_eval_count and (
                thousand_eval_count[size] < thousand_threshold
            )

            if should_save_color and random.random() < 0.5:
                ImageManager.save_image(
                    self.color_dir / color_size / file_name,
                    augmented_image_data.rotated_image,
                )
                color_eval_count[color_size] += 1
            elif should_save_thousand:
                ImageManager.save_image(
                    self.thousand_dir / size / file_name,
                    augmented_image_data.rotated_image,
                )
                thousand_eval_count[size] += 1
            else:
                leftover_aug_imdata_list.append(augmented_image_data)

        eval_set_service.create_color_eval(self.item, color_eval_count)
        eval_set_service.create_thousand_eval(self.item, thousand_eval_count)

        return leftover_imdata_list, leftover_aug_imdata_list
