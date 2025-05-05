from pathlib import Path
from tensorflow import keras
from keras import models

from constants.folder_names import ModelDatasetFolderNames
from constants.tensorflow_model import DatasetModes, HyperParameters, ModelFiles
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager
from utils.ai_model.tensorflow_model import TensorflowModel


def start_training(item: str, input_size: int, file_name: str) -> None:
    """Starts the training process for an AI model."""
    item_model_dir, dataset_dir = setup_training_environment(item)

    train_dataset, _ = TensorflowModel.prepare_dataset(
        dataset_dir / ModelDatasetFolderNames.TRAIN, input_size, shuffle=True
    )
    validation_dataset, _ = TensorflowModel.prepare_dataset(
        dataset_dir / ModelDatasetFolderNames.VALIDATION, input_size
    )

    callbacks = TensorflowModel.create_callbacks()
    model = TensorflowModel.build_static_model(input_size, len(DatasetModes))
    model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=HyperParameters.EPOCHS,
        verbose=1,
        callbacks=callbacks,
    )

    save_model_and_class_txt(model, list(DatasetModes), item_model_dir, file_name)


def setup_training_environment(item: str) -> tuple[Path, Path]:
    """Sets up the necessary environments for training."""
    model_json_dir = dm.json_dir / ModelFiles.TRAINING_JSON
    FileManager.write_json(model_json_dir, [])

    item_model_dir = dm.model_dir / item
    dm.create_directory(item_model_dir)
    dataset_dir = dm.images_dir / ModelDatasetFolderNames.DATASET / item

    return item_model_dir, dataset_dir


def save_model_and_class_txt(
    trained_model: models.Sequential,
    dataset_class_names: list[str],
    output_dir: Path,
    file_name: str,
) -> None:
    """Saves the trained model and a text file containing class names."""
    # TODO: change to use TFModel for saving
    model_path = output_dir / f"{file_name}{ModelFiles.MODEL_EXT}"
    trained_model.save(model_path)

    txt_content = "\n".join(
        f"{i} {label}" for i, label in enumerate(dataset_class_names)
    )
    txt_path = output_dir / f"{file_name}{ModelFiles.LABEL_EXT}"
    FileManager.write_txt(txt_path, txt_content)
