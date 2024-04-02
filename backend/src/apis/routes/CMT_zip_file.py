import os
import zipfile
from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel


router = APIRouter()

class Directory:
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    image_path = os.path.join(base_path, "images")
    dataset_path = os.path.join(base_path, "dataset")
    eval_path = os.path.join(base_path, "evaluation")
    results_path = os.path.join(base_path, "results")
    models_path = os.path.join(base_path, "models")  
    old_path = os.path.join(dataset_path, "old")

class ModelName(BaseModel):
    modelname: str

dire = Directory.models_path
temp_folder = 'temp'

@router.post("/zip_model/")
async def zip_model(model: ModelName):
    model_base_path = os.path.join(dire, temp_folder, model.modelname)

    txt_file_path = f"{model_base_path}.txt"
    keras_file_path = f"{model_base_path}.keras"

    if not os.path.exists(txt_file_path) or not os.path.exists(keras_file_path):
        raise HTTPException(status_code=404, detail="Model files not found")

    zip_file_path = f"{model_base_path}.zip"

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write(txt_file_path, arcname=os.path.basename(txt_file_path))
        zipf.write(keras_file_path, arcname=os.path.basename(keras_file_path))

    # Return the ZIP file
    return FileResponse(zip_file_path, filename=os.path.basename(zip_file_path), media_type='application/zip')