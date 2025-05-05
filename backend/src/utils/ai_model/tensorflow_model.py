import os

os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import math
import numpy as np
import onnx
import random
import tf2onnx
from pathlib import Path
from tensorflow import data, keras
from keras import layers, losses, models, optimizers, utils, callbacks as cb

from constants.folder_names import ModelDatasetFolderNames
from constants.tensorflow_model import DatasetModes, HyperParameters
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager
from utils.ai_model.epoch_history_callbacks import EpochHistory


# TODO: pytest
class TensorflowModel:
    """A utility class for building, loading, and preparing TensorFlow models and datasets."""

    @staticmethod
    def build_static_model(input_size: int, output_size: int) -> models.Sequential:
        """Builds a static convolutional neural network model.

        Args:
            input_size: The size of the input images (height and width).
            output_size: The number of output classes.

        Returns:
            A Keras Sequential model.
        """
        ker = (3, 3)
        ker2 = (1, 1)
        input_shape = (input_size, input_size, 3)

        model = models.Sequential(
            [
                layers.Input(shape=input_shape),
                layers.Rescaling(1.0 / 255),
                layers.RandomFlip("horizontal_and_vertical", seed=HyperParameters.SEED),
                layers.Conv2D(16, kernel_size=ker, activation="relu", padding="same"),
                layers.Conv2D(32, kernel_size=ker2, activation="relu", padding="same"),
                layers.MaxPool2D(2, 2),
                layers.Conv2D(64, kernel_size=ker, activation="relu", padding="same"),
                layers.Conv2D(128, kernel_size=ker2, activation="relu", padding="same"),
                layers.BatchNormalization(),
                layers.MaxPool2D(3, 2),
                layers.Conv2D(256, kernel_size=ker, activation="relu", padding="same"),
                layers.Conv2D(512, kernel_size=ker2, activation="relu", padding="same"),
                layers.AveragePooling2D(3),
                layers.Flatten(),
                layers.Dropout(0.3),
                layers.Dense(output_size, activation="softmax"),
            ]
        )

        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss=losses.SparseCategoricalCrossentropy(),
            metrics=["accuracy"],
        )

        return model

    @staticmethod
    def create_callbacks() -> list[cb.Callback]:
        """Creates a list of training callbacks.

        Returns:
            A list of Keras Callback objects.
        """
        early_stopping = cb.EarlyStopping(
            monitor="val_loss", patience=7, verbose=1, mode="min"
        )
        reduce_lr = cb.ReduceLROnPlateau(
            monitor="val_loss", factor=0.2, patience=3, min_lr=1e-5, verbose=1
        )
        epoch_history = EpochHistory()

        return [early_stopping, reduce_lr, epoch_history]

    @staticmethod
    def save_onnx_model(model: models.Sequential, ai_model_path: Path) -> bool:
        """Converts and saves a Keras Sequential model to ONNX format.

        Args:
            model: The Keras Sequential model to save.
            ai_model_path: The path where the ONNX model will be saved.

        Returns:
            True if the model was saved successfully.
        """
        try:
            onnx_model, _ = tf2onnx.convert.from_keras(model)
            onnx.save_model(onnx_model, ai_model_path)
            return True
        except Exception as e:
            print(f"Error saving ONNX model: {e}")
            return False

    @staticmethod
    def load_model(ai_model_path: Path) -> models.Sequential:
        """Loads a Keras Sequential model from a given path.

        Args:
            ai_model_path: The pathlib.Path object pointing to the model file.

        Returns:
            A loaded Keras Sequential model.

        Raises:
            FileNotFoundError: If the model file does not exist.
        """
        ai_model_file_name = ai_model_path.name
        if not ai_model_path.exists():
            raise FileNotFoundError(
                f"{ai_model_file_name} not found in {ai_model_path}"
            )

        return models.load_model(ai_model_path)

    @staticmethod
    def prepare_dataset(
        dataset_dir: Path,
        input_size: int,
        labels: str = "inferred",
        shuffle: bool = False,
    ) -> tuple[data.Dataset, list[str]]:
        """Prepares a TensorFlow dataset from image files in a directory.

        Args:
            dataset_dir: The pathlib.Path object pointing to the dataset directory.
                         Subdirectories are expected to represent class labels.
            input_size: The desired size (height and width) of the input images.
            labels: How to obtain the image labels. Defaults to "inferred"
                                    (from subdirectory names).
            shuffle: Whether to shuffle the dataset. Defaults to False.

        Returns:
           A TensorFlow Dataset object and a NumPy array of file paths.

        Raises:
            FileNotFoundError: If the dataset directory is empty or does not exist.
        """
        if not dataset_dir.exists() or not any(dataset_dir.iterdir()):
            raise FileNotFoundError(
                f"Warning: The directory '{dataset_dir}' is empty or doesn't exist."
            )

        dataset = utils.image_dataset_from_directory(
            dataset_dir,
            labels=labels,
            label_mode="int",
            batch_size=HyperParameters.BATCH_SIZE,
            image_size=[input_size, input_size],
            seed=HyperParameters.SEED,
            shuffle=shuffle,
        )

        AUTOTUNE = data.AUTOTUNE
        if shuffle:
            prefetched_dataset = (
                dataset.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
            )
        else:
            prefetched_dataset = dataset.cache().prefetch(buffer_size=AUTOTUNE)

        return prefetched_dataset, np.array(dataset.file_paths)

    @staticmethod
    def train_validation_split(dataset_dir: Path) -> None:
        """Splits a dataset directory into training and validation sets.

        Args:
            dataset_dir: The main dataset directory. Subdirectories within are expected to represent class labels.
            validation_split_ratio: The proportion of data (20%) to move to the validation set.
        """
        train_dir = dataset_dir / ModelDatasetFolderNames.TRAIN
        validation_dir = dataset_dir / ModelDatasetFolderNames.VALIDATION
        dm.create_directory(validation_dir, True)
        for folder in DatasetModes:
            train_file_paths = dm.list_png_paths(train_dir / folder)
            split_qty = math.ceil(len(train_file_paths) * 0.2)
            to_move_file_paths = random.sample(train_file_paths, split_qty)
            FileManager.move_files_to_dir(
                validation_dir / folder, to_move_file_paths, True
            )
