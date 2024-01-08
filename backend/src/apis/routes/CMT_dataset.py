from fastapi import APIRouter
from pydantic import BaseModel
from apis.CMT.training.dataset import create_image_dataset

class DatasetInfo(BaseModel):
    train_dataset_info: dict
    validation_dataset_info: dict

router = APIRouter()


@router.post("/process_dataset/", response_model=DatasetInfo)
async def process_dataset(selected_dir: str):
    try:
        (train_ds, train_info), (validation_ds, validation_info) = create_image_dataset(selected_dir)
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

    return {
        "train_dataset_info": train_info,
        "validation_dataset_info": validation_info
    }


