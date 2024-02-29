import os
from tensorflow import keras, data
from keras.preprocessing import image_dataset_from_directory

from apis.utils.directory import dire
from core.config import settings


def create_image_dataset(sel_folder):
    """
    Main Function to Creates image datasets for training and validation.
    """
    sel_folder = os.path.join(dire.dataset_path, sel_folder)

    train_dir = os.path.join(sel_folder, "training")
    validation_dir = os.path.join(sel_folder, "validation")

    train_ds, train_info = get_dataset_info(train_dir, True)
    validation_ds, validation_info = get_dataset_info(validation_dir)

    AUTOTUNE = data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    validation_ds = validation_ds.cache().prefetch(buffer_size=AUTOTUNE)

    return train_ds, train_info, validation_ds, validation_info


def get_dataset_info(dire, shuffle=False):
    """
    Returns information about the dataset if it exists, else returns an empty info.
    """
    # Directly create the datasets
    batch_size = settings.BATCH_SIZE
    image_size = settings.IMAGE_SIZE
    seed = settings.SEED

    ds = None
    info = {"count": 0, "classes": [], "class_counts": {}}

    if os.path.exists(dire):
        ds = image_dataset_from_directory(
            dire,
            labels="inferred",
            batch_size=batch_size,
            image_size=image_size,
            seed=seed,
            shuffle=shuffle,
        )
        class_names = ds.class_names
        file_paths = ds.file_paths
        info = {
            "count": len(file_paths),
            "classes": class_names,
            "class_counts": len(class_names),
        }
    return ds, info
