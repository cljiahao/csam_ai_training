import os
from zipfile import ZipFile
from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from starlette.background import BackgroundTask

from apis.utils.directory import dire

router = APIRouter()


class ModelName(BaseModel):
    m_path: str


@router.post("/zip_model")
async def zip_model(model: ModelName):
    folder, model_name = model.m_path.split("/")
    model_base_path = os.path.join(dire.models_path, folder, model_name)

    txt_path = f"{model_base_path}.txt"
    keras_path = f"{model_base_path}.h5"

    if not os.path.exists(txt_path) or not os.path.exists(keras_path):
        raise HTTPException(status_code=525, detail="Model files not found")

    zip_path = f"{model_base_path}.zip"

    with ZipFile(zip_path, "w") as zipf:
        zipf.write(txt_path, arcname=os.path.basename(txt_path)[16:])
        zipf.write(keras_path, arcname=os.path.basename(keras_path)[16:])

    return FileResponse(
        zip_path,
        filename=os.path.basename(zip_path),
        media_type="application/zip",
        background=BackgroundTask(os.remove, zip_path),
    )
