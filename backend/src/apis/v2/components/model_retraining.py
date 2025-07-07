from pathlib import Path
from keras import models

from constants.folder_names import ModelDatasetFolderNames, ReTrainFolderName
from constants.tensorflow_model import DatasetModes, HyperParameters, ModelFiles
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager
from utils.ai_model.tensorflow_model import TensorflowModel
from utils.debug import timer


@timer("Start Retraining")
def start_retraining(
    item: str, input_size: int, original_model_name: str, new_file_name: str
) -> None:
    """Starts the re-training process for trained AI model."""
    item_model_dir, retrain_dataset_dir = setup_retraining_environment(item)
    prepare_retrain_dataset(item, retrain_dataset_dir)

    original_model_path = (
        item_model_dir / f"{original_model_name}{ModelFiles.H5_MODEL_EXT}"
    )

    if not original_model_path.exists():
        raise FileNotFoundError(f"Model file not found: {original_model_path}")

    model = TensorflowModel.prepare_model_for_retraining(original_model_path)

    output_shape = model.layers[-1].output_shape
    expected_classes = len(DatasetModes)

    if output_shape[-1] != expected_classes:
        raise ValueError(
            f"Model has incompatible output shape: expected {expected_classes} classes, got {output_shape[-1]}"
        )
    train_dataset, _ = TensorflowModel.prepare_dataset(
        retrain_dataset_dir / ModelDatasetFolderNames.TRAIN, input_size, shuffle=True
    )
    validation_dataset, _ = TensorflowModel.prepare_dataset(
        retrain_dataset_dir / ModelDatasetFolderNames.VALIDATION, input_size
    )
    callbacks = TensorflowModel.create_callbacks(is_train=False)

    model.fit(
        train_dataset,
        validation_data=validation_dataset,
        epochs=HyperParameters.EPOCHS,
        verbose=1,
        callbacks=callbacks,
    )
    save_model_and_class_txt(model, item_model_dir, new_file_name)


@timer("Setup Retraining Environment")
def setup_retraining_environment(item: str) -> tuple[Path, Path]:
    """Sets up the necessary environments for retraining."""
    model_json_dir = dm.json_dir / ModelFiles.RETRAINING_JSON
    FileManager.write_json(model_json_dir, [])

    item_model_dir = dm.model_dir / item
    dm.create_directory(item_model_dir)
    retrain_dataset_dir = dm.images_dir / ModelDatasetFolderNames.RETRAIN_DATASET / item
    dm.create_directory(retrain_dataset_dir)
    return item_model_dir, retrain_dataset_dir


@timer("Prepare Retrain Dataset")
def prepare_retrain_dataset(item: str, retrain_dataset_dir: Path) -> None:
    """Prepares datasets from retrain folder for model retraining."""
    retrain_dir = dm.images_dir / ReTrainFolderName.RETRAIN / item
    train_dir = retrain_dataset_dir / ModelDatasetFolderNames.TRAIN
    dm.create_subdirectories(train_dir, DatasetModes, True)
    for mode in DatasetModes:
        source_dir = retrain_dir / mode
        if source_dir.exists():
            source_files = dm.list_png_paths(source_dir)
            if source_files:
                FileManager.copy_files_to_dir(train_dir / mode, source_files)
    TensorflowModel.train_validation_split(retrain_dataset_dir)


def save_model_and_class_txt(
    model: models.Sequential,
    output_dir: Path,
    file_name: str,
) -> None:
    """Saves the trained model and a text file containing class names."""
    model_path = output_dir / f"{file_name}{ModelFiles.H5_MODEL_EXT}"
    txt_path = output_dir / f"{file_name}{ModelFiles.LABEL_EXT}"

    TensorflowModel.save_model(model, model_path)
    TensorflowModel.save_class_txt(list(DatasetModes), txt_path)
