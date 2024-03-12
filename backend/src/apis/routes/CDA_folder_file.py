import os
import random
from pydantic import BaseModel
from fastapi import APIRouter

from apis.utils.directory import dire
from apis.CDA.main import get_files


router = APIRouter()


@router.get("/item_type")
def get_item_type():
    if os.path.exists(dire.image_path):
        return os.listdir(dire.image_path)


class getRandomImg(BaseModel):
    item: str
    no_of_img: int


@router.post("/random_img")
def random_img(rand: getRandomImg):
    files = get_files(rand.item, True)

    file_list = []
    for i in range(rand.no_of_img):
        key, arr = random.sample(sorted(files.items()), 1)[0]
        file_name = random.sample(arr, 1)[0]
        file_list.append(f"{key}/{file_name}")

    return file_list


class getRandomCount(BaseModel):
    item: str


@router.post("/random_count")
def random_count(rand: getRandomCount):
    files = get_files(rand.item, False)

    file_count = {}

    path = os.path.join(dire.image_path, rand.item)
    for fol in os.listdir(path):
        file_count[fol] = {}
        fol_dict = {k: v for k, v in files.items() if fol in k}
        key, arr = random.sample(sorted(fol_dict.items()), 1)[0]
        file_name = random.sample(arr, 1)[0]
        file_count[fol]["file_path"] = f"{key}/{file_name}"
        file_count[fol]["count"] = sum(
            [len(files[a]) for a in files.keys() if fol in a]
        )

    return file_count
