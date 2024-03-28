import os
import math
import random
import numpy as np
from shutil import copytree
from concurrent.futures import ThreadPoolExecutor

from apis.CDA.utils.masking import retrieve_roi, superimpose
from core.config import settings


def augmenting(images_path, ds_path, template_dict):

    for base_type in settings.BASE_TYPES:
        if base_type in template_dict:
            base_path = os.path.join(images_path, base_type)
            base_count = template_dict[base_type]["count"]
            del template_dict[base_type]
    base_file_list = os.listdir(base_path)

    for key, value in template_dict.items():
        folder_path = os.path.join(ds_path, "training", key)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        if key not in settings.G_TYPES:
            no_of_samples = math.ceil(
                int(base_count) / (len(template_dict) * value["count"])
            )
            for template in value["template"]:
                sample = random.sample(base_file_list, no_of_samples)
                with ThreadPoolExecutor(10) as exe:
                    _ = [
                        exe.submit(
                            superimpose,
                            base_path,
                            folder_path,
                            file_name,
                            template,
                            f"Aug_{file_name}",
                        )
                        for file_name in sample
                    ]
        else:
            copytree(
                os.path.join(images_path, key),
                os.path.join(folder_path),
                dirs_exist_ok=True,
            )


def templating(root, file_names, range):

    res = []

    Col_LL = np.array(
        [int(vx) for kx, vx in range["hsv"].items() if kx[0] == "L"],
        dtype=np.uint8,
    )
    Col_UL = np.array(
        [int(vy) for ky, vy in range["hsv"].items() if ky[0] == "H"],
        dtype=np.uint8,
    )

    if root.split(os.sep)[-1] not in settings.G_TYPES + settings.BASE_TYPES:

        # Benchmark: without thread - 61.20s, with thread: 18.92s
        with ThreadPoolExecutor(10) as exe:
            _ = [
                exe.submit(
                    retrieve_roi, os.path.join(root, f_name), res, Col_LL, Col_UL
                )
                for f_name in file_names
            ]

    return {"count": len(file_names), "template": res}
