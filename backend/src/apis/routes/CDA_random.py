import os
import time
import random
from fastapi import APIRouter
from fastapi.responses import FileResponse

from apis.utils.directory import dire
from apis.CDA.main import get_files


router = APIRouter()


@router.get("/random/{no_of_img}")
def random_img(no_of_img: int):
    files = get_files(True)

    file_list = []
    for i in range(no_of_img):
        key, arr = random.sample(sorted(files.items()), 1)[0]
        file_name = random.sample(arr, 1)[0]
        file_list.append(f"{key}/{file_name}")

    return {"file_list": file_list}


@router.get("/get_image/{src:path}")
def get_image(src: str):
    file_path = os.path.join(dire.image_path, src)
    return FileResponse(file_path)
