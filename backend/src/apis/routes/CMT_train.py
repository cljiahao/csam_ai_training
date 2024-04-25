import os
import asyncio
from fastapi import APIRouter
from pydantic import BaseModel
from datetime import datetime as dt

from apis.routes.CMT_folder_file import dire
from apis.CMT.main import training
from apis.CMT.training.dataset import create_image_dataset
from core.read_write import read_json, write_json


router = APIRouter()


class trainModel(BaseModel):
    item: str
    folder: str
    model: str
    epochs: int
    callbacks: dict


@router.post("/train_model")
async def train_model(selected: trainModel):

    # TODO: Check if files / folders exists
    train_ds, train_info, validation_ds, validation_info = create_image_dataset(
        selected.item, selected.folder
    )

    file_name = f"{dt.now().strftime('%Y%m%d_%H%M%S')}_{selected.item}"

    with open(os.path.join(dire.models_path, "temp", f"{file_name}.txt"), "w") as f:
        for i, cat in enumerate(train_info["classes"]):
            f.write(f"{i} {cat}\n")

    # Delete old models file if folder more than 20
    temp_path = os.path.join(dire.models_path, "temp")
    folders = os.listdir(temp_path)
    if 20 < len(folders):
        to_del = folders[:2]
        for j in to_del:
            os.remove(os.path.join(temp_path, j))

    # Reset json file if error
    train_set = read_json(os.path.join(dire.json_path, "train.json"))
    train_set["Frontend"]["status"] = "complete"
    write_json(os.path.join(dire.json_path, "train.json"), train_set)

    asyncio.run_coroutine_threadsafe(
        training(selected, file_name, train_ds, train_info, validation_ds),
        loop=asyncio.get_running_loop(),
    )
    return f"temp/{file_name}"


@router.get("/current_epoch")
def current_epoch():
    train_set = read_json(os.path.join(dire.json_path, "train.json"))
    return train_set["Frontend"]
