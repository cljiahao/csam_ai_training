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


def aug_process(input):
    start = time.time()
    base_path = os.path.join(dire.image_path, input.item)
    folders_list = os.listdir(base_path)

    if not any(x in folders_list for x in ["G", "g", "good", "Good"]):
        raise Exception(f"[G, g, good, Good] folder path missing to augment")

    for i in folders_list:
        if i in ["G", "g", "good", "Good"]:
            g_path = os.path.join(base_path, i)

            file_names = os.listdir(g_path)
            image_fols = folders_list
            if len(file_names) < int(input.entry["target"]):
                raise Exception(
                    f"Number of files in G path, {len(file_names)}, is less than {input.entry['target']}"
                )

    new_version = zip_check_dataset(os.path.join(dire.dataset_path, input.item))
    time_print(start, "Zipping old datasets")
    dataset_fols, template_dict, count_dict = get_dicts(
        input.item, new_version, image_fols, input.range
    )
    time_print(start, "Copying Files and Templating all NGs")
    augmenting(g_path, file_names, template_dict, count_dict, dataset_fols, input.entry)
    time_print(start, "Augmenting all NGs")
    train_val_split(dataset_fols, image_fols, input.entry)
    time_print(start, "Train Val Split")
