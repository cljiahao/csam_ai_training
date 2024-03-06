import asyncio
from fastapi import APIRouter
from pydantic import BaseModel

from apis.CMT.main import training
from core.read_json import read_config


router = APIRouter()


class trainModel(BaseModel):
    item: str
    folder: str
    epochs: int
    callbacks: dict


@router.post("/train_model")
async def train_model(selected: trainModel):
    print(selected)
    asyncio.run_coroutine_threadsafe(
        training(selected.item, selected.folder, selected.epochs, selected.callbacks),
        loop=asyncio.get_running_loop(),
    )
    return {"status": "started"}


@router.get("/current_epoch")
def current_epoch():
    train_set = read_config("./core/json/train.json")
    return train_set["Frontend"]
