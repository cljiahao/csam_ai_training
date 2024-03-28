import os
import math
import random
from shutil import move, copyfile


def train_val_split(ds_path, item_fol_list, split):
    split_perc = float(split["split"]) / 100

    for fol in item_fol_list:
        train_path = os.path.join(ds_path, "training", fol)
        val_path = os.path.join(ds_path, "validation", fol)
        if not os.path.exists(val_path):
            os.makedirs(val_path)

        train_files = os.listdir(train_path)
        split_qty = math.ceil(len(train_files) * split_perc)
        file_names = random.sample(train_files, split_qty)
        for file in file_names:
            move(
                os.path.join(train_path, file),
                os.path.join(val_path, file),
                copy_function=copyfile,
            )
