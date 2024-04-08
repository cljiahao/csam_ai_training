import os
import zipfile
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from apis.utils.directory import dire

router = APIRouter()

class ModelName(BaseModel):
    modelname: str

@router.post("/zip_model/")
async def zip_model(model: ModelName):
    model_base_path = os.path.join(dire.temp_path, model.modelname)

    txt_file_path = f"{model_base_path}.txt"
    keras_file_path = f"{model_base_path}.keras"

    if not os.path.exists(txt_file_path) or not os.path.exists(keras_file_path):
        raise HTTPException(status_code=404, detail="Model files not found")

    zip_file_path = f"{model_base_path}.zip"

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(txt_file_path, arcname=os.path.basename(txt_file_path))
        zipf.write(keras_file_path, arcname=os.path.basename(keras_file_path))

    return FileResponse(zip_file_path, filename=os.path.basename(zip_file_path), media_type='application/zip')