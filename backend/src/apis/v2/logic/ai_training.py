from pathlib import Path
from sqlalchemy.orm import Session
from tensorflow import keras, data
from keras import preprocessing as pp


from apis.v2.helpers.processor.train_processor import TrainProcessor
from constants.tf_model import TFModel
from core.exceptions import NoResultsFound
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager
from db.services.image_settings import ImageSettingsService
from schemas.ai_model import DatasetInfo


def pre_process_dataset(
    file_name: str, item: str, db: Session
) -> tuple[int, int, list, list]:
    image_settings_service = ImageSettingsService(db)
    image_settings = image_settings_service.read_image_settings(item)

    if image_settings is None:
        raise NoResultsFound(
            f"Image settings for '{item}' not found in API or database."
        )

    input_size = image_settings.crop_size

    train_processor = TrainProcessor(item)

    train_ds, train_info = get_dataset_info(train_processor.train_dir, input_size, True)
    validation_ds, _ = get_dataset_info(train_processor.validation_dir, input_size)

    txt_content = "\n".join(
        f"{i} {label}" for i, label in enumerate(train_info.classes)
    )
    FileManager.write_txt(dm.model_dir / f"{file_name}.txt", txt_content)

    AUTOTUNE = data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    validation_ds = validation_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return input_size, train_info.class_counts, train_ds, validation_ds


def get_dataset_info(
    directory: Path, input_size: int, shuffle=False
) -> tuple[list, DatasetInfo]:
    """Returns information about the dataset if it exists, else returns an empty info."""

    dataset = None
    info = DatasetInfo(count=0, classes=[], class_counts={})

    if not directory.exists() or not any(directory.iterdir()):
        raise FileNotFoundError(
            f"Warning: The directory '{directory}' is empty or doesn't exist."
        )

    dataset = pp.image_dataset_from_directory(
        directory,
        labels="inferred",
        batch_size=TFModel.BATCH_SIZE.value,
        image_size=input_size,
        seed=TFModel.SEED.value,
        shuffle=shuffle,
    )
    class_names = dataset.class_names
    file_paths = dataset.file_paths

    info = DatasetInfo(
        count=len(file_paths), classes=class_names, class_counts=len(class_names)
    )

    return dataset, info
