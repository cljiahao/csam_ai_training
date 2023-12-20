import os
import random
from fastapi import APIRouter
from fastapi.responses import FileResponse
import numpy as np

from apis.CDA.utils.directory import dire
from apis.CDA.main import aug_process
from core.read_json import read_config, write_config

router = APIRouter()


@router.get("/random/{no_of_img}")
def random_img(no_of_img: int):
    augment_set = read_config("./core/json/augment.json")
    files = {}
    for fol in os.listdir(dire.image_path):
        if fol.lower() != "g":
            for file in os.listdir(os.path.join(dire.image_path, fol)):
                if file.split(".")[-1] not in augment_set["format"]:
                    files[f"{fol}/{file}"] = os.listdir(
                        os.path.join(dire.image_path, fol, file)
                    )
                else:
                    if fol not in files.keys():
                        files[fol] = []
                    files[fol].append(file)

    file_list = []
    for i in range(no_of_img):
        key, arr = random.sample(files.items(), 1)[0]
        file_name = random.sample(arr, 1)[0]
        file_list.append(f"{key}/{file_name}")

    return {"file_list": file_list}


@router.get("/images/{src:path}")
def get_image(src: str):
    file_path = os.path.join(dire.image_path, src)
    return FileResponse(file_path)


@router.get("/get_trackbar")
def get_trackbar():
    trackbar_val = read_config("./core/json/trackbar.json")
    return {"trackbar": trackbar_val}


@router.post("/set_trackbar")
def set_trackbar(range: dict):
    try:
        write_config("./core/json/trackbar.json", range)
        alert = {
            "title": "Range Settings Saved",
            "text": "Confirm to Continue",
            "icon": "success",
            "confirmButtonText": "Confirm",
        }
    except:
        alert = {
            "title": "Range Failed to Save!",
            "text": "Please Try Again",
            "icon": "error",
            "confirmButtonText": "Confirm",
        }
    return alert


@router.post("/process_img")
def process_img(range: dict):
    try:
        write_config("./core/json/trackbar.json", range)
        aug_process()
        alert = {
            "title": "Image Augmented",
            "text": "Confirm to Continue",
            "icon": "success",
            "confirmButtonText": "Confirm",
        }

    except Exception as e:
        print(e)
        alert = {
            "title": "Image Failed to Augment!",
            "text": "Please Try Again",
            "icon": "error",
            "confirmButtonText": "Confirm",
        }
    return alert
