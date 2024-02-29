import os
import time

from apis.utils.directory import dire, zip_check_dataset
from apis.utils.misc import time_print
from apis.CDA.utils.directory import get_dicts
from apis.CDA.utils.dataset import train_val_split
from apis.CDA.utils.augment import augmenting


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


def get_files(good):
    files = {}
    for fol in os.listdir(dire.image_path):
        if good and fol in ["G", "g", "good", "Good"]:
            continue
        for file in os.listdir(os.path.join(dire.image_path, fol)):
            if file.split(".")[-1] not in ["jpg", "jpeg", "png", "tiff"]:
                files[f"{fol}/{file}"] = os.listdir(
                    os.path.join(dire.image_path, fol, file)
                )
            else:
                if fol not in files.keys():
                    files[fol] = []
                files[fol].append(file)

    return files
