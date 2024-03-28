import os
import cv2
import numpy as np

from core.read_json import read_config


def superimpose(base_path, folder_path, file_name, template, new_f_name):

    img = cv2.imread(os.path.join(base_path, file_name))
    _, chip_mask = removed_bg(img)
    gray = cv2.cvtColor(template.copy(), cv2.COLOR_BGR2GRAY)
    _, template_mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    mask = cv2.bitwise_and(chip_mask, chip_mask, mask=template_mask)
    img[mask > 0] = 0
    img += cv2.bitwise_and(template, template, mask=mask)

    cv2.imwrite(os.path.join(folder_path, new_f_name), img)


def retrieve_roi(file_path, res, Col_LL, Col_UL):
    img = cv2.imread(file_path)
    defect, _ = removed_bg(img)
    hsv = cv2.cvtColor(defect, cv2.COLOR_BGR2HSV_FULL)

    mask_def = cv2.inRange(hsv, Col_LL, Col_UL)
    temp_def = cv2.bitwise_and(defect, defect, mask=mask_def)

    res.append(temp_def)


def removed_bg(img):
    mask = bg_masking(img.copy())
    contours, hier = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    defect, chip_mask = get_largest(img.copy(), contours)

    return defect, chip_mask


def bg_masking(img):
    trackbar_set = read_config("./core/json/trackbar.json")

    background = np.where(
        (img[:, :, 0] >= 130) & (img[:, :, 1] >= 130) & (img[:, :, 2] >= 130)
    )
    img[background] = (255, 255, 255)  # Convert background to white for better contrast

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    th, ret = cv2.threshold(
        gray, int(trackbar_set["mask"]["Thresh"]), 255, cv2.THRESH_BINARY_INV
    )
    morph = cv2.morphologyEx(
        ret, cv2.MORPH_CLOSE, (3, 3)
    )  # Close off any small poor scannings
    morph = cv2.morphologyEx(
        morph,
        cv2.MORPH_ERODE,
        np.ones(
            (
                int(trackbar_set["mask"]["Erode_x"]),
                int(trackbar_set["mask"]["Erode_y"]),
            ),
            np.uint8,
        ),
    )

    return morph


def get_largest(img, cnts):
    area = 0
    for c in cnts:
        if area < cv2.contourArea(c):
            area = cv2.contourArea(c)
            maxc = c

    blank = np.zeros(img.shape[:2], np.uint8)
    chipmask = cv2.drawContours(blank, [maxc], -1, (255, 255, 255), -1)
    chipmask = cv2.dilate(chipmask, np.ones((3, 3), np.uint8))
    img[chipmask == 0] = [192, 192, 192]

    return img, chipmask
