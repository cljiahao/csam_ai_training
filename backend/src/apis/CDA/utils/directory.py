import os
import time
from shutil import copyfile
from concurrent.futures import ThreadPoolExecutor

from apis.CDA.utils.augment import templating
from apis.utils.directory import dire


def get_dicts(new_version, image_fols):
    count_dict = {}
    template_dict = {}

    for fol in image_fols:
        dataset_fols = create_dataset_fol(new_version, fol)

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
        print(
            f"{fol} with {sum([len(count_dict[a]) for a in count_dict.keys() if fol in a])} took {round(time.time()-start,2)} secs"
        )
    return dataset_fols, template_dict, count_dict


def create_dataset_fol(new_version, fol):
    dataset_fols = {}
    for i in ["training", "validation"]:
        dataset_fols[f"{i}_{fol}"] = os.path.join(
            dire.dataset_path, new_version, i, fol
        )
        if not os.path.exists(dataset_fols[f"{i}_{fol}"]):
            os.makedirs(dataset_fols[f"{i}_{fol}"])
    return dataset_fols


def check_path(template_dict, count_dict, ds_path, fol, in_fol=False):
    path = (
        os.path.join(dire.image_path, fol, in_fol)
        if in_fol
        else os.path.join(dire.image_path, fol)
    )

    key = f"{fol}_{in_fol}" if in_fol else fol
    template_dict[key] = {"mask": [], "temp": []}
    if key.lower() != "g":
        count_dict[key] = 0

    with ThreadPoolExecutor(10) as exe:
        _ = [
            exe.submit(
                template_arr,
                template_dict,
                count_dict,
                path,
                ds_path,
                key,
                file,
            )
            for file in os.listdir(path)
        ]


def template_arr(template_dict, count_dict, path, ds_path, key, file):
    file_path = os.path.join(path, file)
    copyfile(file_path, os.path.join(ds_path, file))
    if key.lower() != "g":
        count_dict[key] += 1
        mask_def, temp_def = templating(file_path)
        template_dict[key]["mask"].append(mask_def)
        template_dict[key]["temp"].append(temp_def)
