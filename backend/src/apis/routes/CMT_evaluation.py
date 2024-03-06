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

    if f"{resp.model}.h5" in os.listdir(dire.models_path):
        model = Models.load_model(os.path.join(dire.models_path, f"{resp.model}.h5"))

    labels = []
    with open(os.path.join(dire.models_path, f"{resp.model}.txt")) as f:
        data = f.readlines()
        for i in data:
            labels.append(i.split()[-1])

    results = evaluation(resp.item, model, labels)

    return results
