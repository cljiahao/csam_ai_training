import os
import cv2
import math
import random
import numpy as np

from apis.CDA.utils.masking import bg_masking, get_largest


def removed_bg(img):
    mask = bg_masking(img.copy())
    contours, hier = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    defect, chip_mask = get_largest(img.copy(), contours)

    return defect, chip_mask


def templating(img_path, range):

    Col_LL = np.array(
        [int(vx) for kx, vx in range["hsv"].items() if kx[0] == "L"],
        dtype=np.uint8,
    )
    Col_UL = np.array(
        [int(vy) for ky, vy in range["hsv"].items() if ky[0] == "H"],
        dtype=np.uint8,
    )
    img = cv2.imread(img_path)
    defect, _ = removed_bg(img)

    hsv = cv2.cvtColor(defect, cv2.COLOR_BGR2HSV_FULL)
    mask_def = cv2.inRange(hsv, Col_LL, Col_UL)
    temp_def = cv2.bitwise_and(defect, defect, mask=mask_def)

    return mask_def, temp_def


def augmenting(g_path, file_names, template_dict, count_dict, dataset_fols, entry):
    for i in ["G", "g", "good", "Good"]:
        if i in count_dict.keys():
            del count_dict[i]
    if sum(count_dict.values()) <= int(entry["target"]) / 2:
        i = 0
        for k, v in count_dict.items():
            no_of_samples = math.ceil(int(entry["target"]) / (len(count_dict) * v) - 1)
            for j, temp_arr in enumerate(template_dict[k]["temp"]):
                sample = random.sample(file_names, no_of_samples)
                for file_name in sample:
                    img = cv2.imread(os.path.join(g_path, file_name))
                    _, chip_mask = removed_bg(img)
                    mask = cv2.bitwise_and(chip_mask, template_dict[k]["mask"][j])
                    img[mask > 0] = 0
                    img += cv2.bitwise_and(temp_arr, temp_arr, mask=mask)
                    cv2.imwrite(
                        os.path.join(
                            dataset_fols[f"training_{k.split('_')[0]}"],
                            f"Aug_{i}_{file_name}",
                        ),
                        img,
                    )
                    i += 1
