import os
import math
import random
from shutil import move, copyfile


def train_val_split(dataset_fols, image_fols, augment_set):
    split_perc = float(augment_set["split"]) / 100

    for fol in image_fols:
        train_path = dataset_fols[f"training_{fol}"]
        val_path = dataset_fols[f"validation_{fol}"]

        train_files = os.listdir(train_path)
        split_qty = math.ceil(len(train_files) * split_perc)
        file_names = random.sample(train_files, split_qty)
        for file in file_names:
            move(
                os.path.join(train_path, file),
                os.path.join(val_path, file),
                copy_function=copyfile,
            )
