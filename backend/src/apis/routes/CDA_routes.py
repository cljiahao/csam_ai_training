import os
import random
from fastapi import APIRouter
from fastapi.responses import FileResponse

from apis.CDA.utils.directory import directory
from core.read_json import read_config

router = APIRouter()


@router.get("/random/{no_of_img}")
def random_img(no_of_img: int):
    fol_list = os.path.join(directory.raw_path, "NG")
    file_list = random.sample(os.listdir(fol_list), no_of_img)
    return {"file_list": file_list}


@router.get("/images/{src}")
def get_image(src: str):
    file_path = os.path.join(directory.raw_path, "NG", src)
    return FileResponse(file_path)


@router.get("/trackbar")
def get_trackbar():
    trackbar_val = read_config("./core/json/trackbar.json")
    return {"trackbar": trackbar_val}


@router.post("/trackbar")
def set_trackbar():
    pass
