import os
from fastapi import APIRouter
from pydantic import BaseModel
from tensorflow import keras
from keras import models as Models

from apis.utils.directory import dire
from apis.CMT.main import evaluation


router = APIRouter()


class response(BaseModel):
    name_model: str


@router.post("/evaluation_folders")
def evaluation_folders(resp: response):

    # if resp.name_model in os.listdir(dire.models_path):
    #     model = Models.load_model(os.path.join(dire.models_path, f"{resp.name_model}.h5"))

    # labels = []
    # with open(os.path.join(dire.models_path, f"{resp.name_model}.txt")) as f:
    #     data = f.readlines()
    #     for i in data:
    #         labels.append(i.split()[-1])

    model = Models.load_model(os.path.join(dire.models_path, "test.h5"))
    labels = []
    with open(os.path.join(dire.models_path, "test.txt")) as f:
        data = f.readlines()
        for i in data:
            labels.append(i.split()[-1])

    results = evaluation(model, labels)

    return results
