import os
import time

from core.read_json import read_config
from apis.CDA.utils.directory import dire, get_dicts
from apis.CDA.utils.dataset import train_val_split, zip_check_dataset
from apis.CDA.utils.augment import augmenting


def time_print(start, func_name) -> None:
    """
    Parameters
    ----------
    start : float
        Start time from previous recording
    func_name : string
        Description for previous recording
    """
    print(f"{func_name} took: {round(time.time()-start,2)} secs")

    return time.time()


def aug_process():
    start = time.time()
    augment_set = read_config("./core/json/augment.json")

    g_path = os.path.join(dire.image_path, "g")
    file_names = os.listdir(g_path)
    image_fols = os.listdir(dire.image_path)
    if len(file_names) < augment_set["target"]:
        raise Exception(
            f"Number of files in G path, {len(file_names)}, is less than {augment_set['target']}"
        )

    new_version = zip_check_dataset()
    time_print(start, "Zipping old datasets")
    dataset_fols, template_dict, count_dict = get_dicts(new_version, image_fols)
    time_print(start, "Copying Files and Templating all NGs")
    augmenting(g_path, file_names, template_dict, count_dict, dataset_fols, augment_set)
    time_print(start, "Augmenting all NGs")
    train_val_split(dataset_fols, image_fols, augment_set)
    time_print(start, "Train Val Split")


def get_files(good):
    files = {}
    for fol in os.listdir(dire.image_path):
        if good and fol.lower() == "g":
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
