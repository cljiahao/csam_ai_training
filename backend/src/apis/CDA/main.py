import os
import time

from apis.utils.directory import dire, zip_check_dataset
from apis.utils.misc import time_print
from apis.CDA.utils.directory import check_exist, get_template
from apis.CDA.utils.augment import augmenting
from apis.CDA.utils.dataset import train_val_split


def get_files(item, good):

    files = {}

    base_path = os.path.join(dire.image_path, item)
    for fol in os.listdir(base_path):
        if good and fol in ["G", "g", "good", "Good"]:
            continue
        folder_path = os.path.join(base_path, fol)
        for file in os.listdir(folder_path):
            if file.split(".")[-1] not in ["jpg", "jpeg", "png", "tiff"]:
                files[f"{item}/{fol}/{file}"] = os.listdir(
                    os.path.join(base_path, fol, file)
                )
            else:
                if fol not in files.keys():
                    files[f"{item}/{fol}"] = []
                files[f"{item}/{fol}"].append(file)

    return files


def aug_process(input):
    start = time.time()

    images_path = check_exist(input.item)
    lap = time_print(start, "Check if folder exists")

    new_version = zip_check_dataset(os.path.join(dire.dataset_path, input.item))
    lap = time_print(lap, "Get latest version and zipping old datasets")

    template_dict = get_template(images_path, input.range)
    lap = time_print(lap, "Reading images folder")

    ds_path = os.path.join(dire.dataset_path, input.item, new_version)
    augmenting(images_path, ds_path, template_dict)
    lap = time_print(lap, "Augmenting all NGs")

    train_val_split(ds_path, template_dict.keys(), input.entry)
    lap = time_print(lap, "Train Val Split")
