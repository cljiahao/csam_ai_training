import os
from fastapi import APIRouter
from pydantic import BaseModel
from tensorflow import keras
from keras import models as Models

from apis.utils.directory import dire
from apis.CMT.main import evaluation


router = APIRouter()


class response(BaseModel):
    model: str
    item: str


@router.post("/evaluate_folders")
def evaluate_folders(resp: response):

    folder, name = resp.model.split("/")

    base_path = os.path.join(dire.models_path, folder)

    if f"{name}.h5" in os.listdir(base_path):
        model = Models.load_model(os.path.join(base_path, f"{name}.h5"))

    if f"{name}.txt" in os.listdir(base_path):
        labels = []
        with open(os.path.join(base_path, f"{name}.txt")) as f:
            data = f.readlines()
            for i in data:
                labels.append(i.split()[-1])

        results = evaluation(resp.item, model, labels)

        return results
