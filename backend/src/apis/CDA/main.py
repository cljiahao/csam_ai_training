import os
import time

from apis.utils.directory import dire, zip_check_dataset
from apis.utils.misc import time_print
from apis.CDA.utils.directory import check_exist, get_template
from apis.CDA.utils.augment import augmenting
from apis.CDA.utils.dataset import train_val_split
from apis.utils.recursive import recursion


def get_files(item):

    files_dict = {}

    images_path = os.path.join(dire.image_path, item)
    for root, dirs, files in os.walk(images_path):
        if len(files):
            recursion(files_dict, root.split(images_path)[-1][1:].split(os.sep), files)

    return files_dict


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
