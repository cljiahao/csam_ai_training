import math
import random
from pathlib import Path

from constants.folder_names import FolderNames
from constants.tf_model import ClassLabel
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager


class TrainProcessor:
    def __init__(self, item: str) -> None:
        self.item = item
        self._initialize_directories()

    def _initialize_directories(self) -> None:
        """Initializes directories for NG, G and Others."""
        dataset_dir = dm.images_dir / FolderNames.DATASET.value / self.item
        self.train_dir = dataset_dir / FolderNames.TRAIN.value
        self.validation_dir = dataset_dir / FolderNames.VALIDATION.value

    def create_directories(self) -> None:
        """Creates necessary directories for evaluation processing."""
        for folder in [ClassLabel.NG.value, ClassLabel.G.value]:
            dm.create_directory(self.train_dir / folder, True)
            dm.create_directory(self.validation_dir / folder, True)

    def train_val_split(
        self, inner_folder_names: list[str], split: float = 0.2
    ) -> None:
        """Split training data into training and validation sets."""
        for folder_names in inner_folder_names:
            train_file_paths = dm.list_png_paths(self.train_dir / folder_names)
            split_qty = math.ceil(len(train_file_paths) * split)
            to_move_file_paths = random.sample(train_file_paths, split_qty)
            FileManager.move_files_to_dir(
                self.validation_dir / folder_names, to_move_file_paths, True
            )
