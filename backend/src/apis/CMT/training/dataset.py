
import tensorflow as tf
from tensorflow.keras.preprocessing import image_dataset_from_directory
from apis.utils.directory import dire
from core.config import Settings    
import os
from collections import Counter

def create_image_dataset(selected_dir):
    batchSize = Settings.BATCHSIZE
    imgSize = Settings.IMAGESIZE
    seed = Settings.SEED

    selected_dir = os.path.join(dire.dataset_path, selected_dir)

    train_dir = os.path.join(selected_dir, 'training')
    validation_dir = os.path.join(selected_dir, 'validation')

    def get_dataset(ds_dir):
        if os.path.exists(ds_dir):
            ds = image_dataset_from_directory(ds_dir, labels="inferred", batch_size=batchSize, image_size=imgSize, seed=seed, shuffle=True)
            return ds
        else:
            return None

    train_ds = get_dataset(train_dir)
    validation_ds = get_dataset(validation_dir)

    # Optionally, you can also return dataset information if needed
    def get_dataset_info(ds):
        if ds:
            class_names = ds.class_names
            file_paths = ds.file_paths
            class_counts = Counter([os.path.split(os.path.split(path)[0])[1] for path in file_paths])
            info = {
                'count': len(file_paths),
                'classes': class_names,
                'class_counts': dict(class_counts)
            }
            return info
        else:
            return {'count': 0, 'classes': [], 'class_counts': {}}

    train_info = get_dataset_info(train_ds)
    validation_info = get_dataset_info(validation_ds)

    return (train_ds, train_info), (validation_ds, validation_info)
