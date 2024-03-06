import os
import time

from apis.utils.directory import dire, zip_check_dataset
from apis.utils.misc import time_print
from apis.CDA.utils.directory import get_dicts
from apis.CDA.utils.dataset import train_val_split

from apis.CDA.utils.augment import augmenting


# TODO: convert the directory reading into recursive


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


def aug_process(range, entry):
    start = time.time()

    for i in ["G", "g", "good", "Good"]:
        if i in os.listdir(dire.image_path):
            g_path = os.path.join(dire.image_path, i)

    file_names = os.listdir(g_path)
    image_fols = os.listdir(dire.image_path)
    if len(file_names) < int(entry["target"]):
        raise Exception(
            f"Number of files in G path, {len(file_names)}, is less than {entry['target']}"
        )

    new_version = zip_check_dataset(dire.dataset_path)
    time_print(start, "Zipping old datasets")
    dataset_fols, template_dict, count_dict = get_dicts(new_version, image_fols, range)
    time_print(start, "Copying Files and Templating all NGs")
    augmenting(g_path, file_names, template_dict, count_dict, dataset_fols, entry)
    time_print(start, "Augmenting all NGs")
    train_val_split(dataset_fols, image_fols, entry)
    time_print(start, "Train Val Split")
