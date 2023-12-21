import os
import time
from shutil import copyfile
from concurrent.futures import ThreadPoolExecutor

from apis.CDA.utils.augment import templating


class Directory:
    base_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    )
    image_path = os.path.join(base_path, "images")
    dataset_path = os.path.join(base_path, "dataset")
    old_path = os.path.join(dataset_path, "old")


dire = Directory


def temp_arr(template_dict, count_dict, path, ds_path, key, file):
    file_path = os.path.join(path, file)
    copyfile(file_path, os.path.join(ds_path, file))
    if key.lower() != "g":
        mask_def, temp_def = templating(file_path)
        count_dict[key] += 1
        template_dict[key]["mask"].append(mask_def)
        template_dict[key]["temp"].append(temp_def)


def check_path(template_dict, count_dict, ds_path, fol, in_fol=False):
    key = f"{fol}_{in_fol}" if in_fol else fol
    template_dict[key] = {"mask": [], "temp": []}
    if key.lower() != "g":
        count_dict[key] = 0
    path = (
        os.path.join(dire.image_path, fol, in_fol)
        if in_fol
        else os.path.join(dire.image_path, fol)
    )
    with ThreadPoolExecutor(10) as exe:
        _ = [
            exe.submit(temp_arr, template_dict, count_dict, path, ds_path, key, file)
            for file in os.listdir(path)
        ]


def get_dicts(image_fols, new_version):
    dataset_fols = {}
    count_dict = {}
    template_dict = {}

    for fol in image_fols:
        for i in ["training", "validation"]:
            dataset_fols[f"{i}_{fol}"] = os.path.join(
                dire.dataset_path, new_version, i, fol
            )
            if not os.path.exists(dataset_fols[f"{i}_{fol}"]):
                os.makedirs(dataset_fols[f"{i}_{fol}"])

        start = time.time()
        if fol.lower() in ["others", "g"]:
            check_path(
                template_dict,
                count_dict,
                dataset_fols[f"training_{fol}"],
                fol,
            )
        else:
            for in_fol in os.listdir(os.path.join(dire.image_path, fol)):
                check_path(
                    template_dict,
                    count_dict,
                    dataset_fols[f"training_{fol}"],
                    fol,
                    in_fol,
                )
        print(f"{fol} took {round(time.time()-start,2)} secs")
    return dataset_fols, template_dict, count_dict
