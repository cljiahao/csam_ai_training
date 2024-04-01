import os
import random
from pydantic import BaseModel
from fastapi import APIRouter

from apis.utils.directory import dire
from apis.CDA.main import get_files
from core.config import settings


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
    files_dict = get_files(rand.item)

    for i in list(files_dict):
        if i in settings.BASE_TYPES + settings.G_TYPES:
            del files_dict[i]

    file_list = []
    for j in range(rand.no_of_img):
        key, values = random.sample(sorted(files_dict.items()), 1)[0]
        if isinstance(values, dict):
            k, values = random.sample(sorted(values.items()), 1)[0]
            key = f"{key}/{k}"
        file_name = random.sample(values, 1)[0]
        file_list.append(f"{rand.item}/{key}/{file_name}")

    return file_list


class getRandom(BaseModel):
    item: str


@router.post("/random_count")
def random_count(rand: getRandom):
    files_dict = get_files(rand.item)

    file_count = {}

    path = os.path.join(dire.image_path, rand.item)
    for fol in os.listdir(path):
        key = fol
        values = files_dict[fol]
        count = len(values)
        if isinstance(values, dict):
            count = len(sum((x for x in values.values()), []))
            k, values = random.sample(sorted(values.items()), 1)[0]
            key = f"{key}/{k}"
        file_name = random.sample(values, 1)[0]
        file_count[fol] = {
            "file_path": f"{rand.item}/{key}/{file_name}",
            "count": count,
        }

    return file_count


@router.post("/randomness")
def randomness(rand: getRandom):
    files_dict = get_files(rand.item)

    for i in list(files_dict):
        if i in settings.BASE_TYPES + settings.G_TYPES:
            if i in settings.BASE_TYPES:
                base_count = len(files_dict[i])
            del files_dict[i]

    for values in files_dict.values():
        count = len(values)
        if isinstance(values, dict):
            count = len(sum((x for x in values.values()), []))

    randomness = round(base_count * count / (10000 * 10), 2) if base_count else 0

    return randomness
