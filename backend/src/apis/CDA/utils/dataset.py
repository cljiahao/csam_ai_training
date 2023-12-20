import os
import math
import random
from shutil import rmtree, make_archive, move, copyfile

from core.read_json import read_config
from apis.CDA.utils.directory import dire


def zip_check_dataset():
    # TODO: Reset version and delete old folder if takes up too much space
    # TODO: Check if there is more than 1 version in folder (Due to user intervention)

    dire.old_path = os.path.join(dire.dataset_path, "old")
    if not os.path.exists(dire.old_path):
        os.makedirs(dire.old_path)
    fol_arr = [fol for fol in os.listdir(dire.dataset_path) if fol != "old"]

    # Archiving / zipping old versions to make way for new version
    # TODO: Speed up processing using threading or asyncio
    if len(fol_arr) > 0:
        latest_version = fol_arr[0]  # Assuming only 1 version in the folder
        make_archive(
            os.path.join(dire.old_path, latest_version),
            "zip",
            dire.dataset_path,
            latest_version,
        )
        rmtree(os.path.join(dire.dataset_path, latest_version))
        new_version = f"V{int(latest_version[1:]) + 1}"
    elif len(os.listdir(dire.old_path)) > 0:
        last_old_version = sorted(os.listdir(dire.old_path), reverse=True)[0]
        lov_name = last_old_version.split(".")[0]
        new_version = f"V{int(lov_name[1:]) + 1}"
    else:
        new_version = "V1"

    return new_version


def train_val_split(dataset_fols, image_fols,augment_set):

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
