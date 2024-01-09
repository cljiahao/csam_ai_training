from ast import Dict
from fastapi import APIRouter, HTTPException, Query, WebSocket
from pydantic import BaseModel
import json
from typing import Dict
from apis.CMT.training.dataset import create_image_dataset
from apis.CMT.training.train_model import train_model
from apis.utils.directory import dire


class DatasetInfo(BaseModel):
    train_dataset_info: dict
    validation_dataset_info: dict

class TrainRequest(BaseModel):
    selected_dir: str
    epochs: int
    early_stopping: bool = False
    best_model: bool = False
    reduce_lr_on_plateau: bool = False
    checkpoint: bool = False

class TrainResponse(BaseModel):
    message: str
    model_save_path: str
    epoch_metrics: list[Dict[str, float]]

router = APIRouter()

@router.post("/process_dataset", response_model=DatasetInfo)
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

@router.post("/train_model", response_model=TrainResponse)
async def train_model_route(
    selected_dir: str = Query(..., description="Directory of the dataset"),
    epochs: int = Query(..., description="Number of training epochs"),
    early_stopping: bool = Query(False, description="Enable early stopping"),
    best_model: bool = Query(False, description="Save the best model"),
    reduce_lr_on_plateau: bool = Query(False, description="Reduce learning rate on plateau"),
    checkpoint: bool = Query(False, description="Enable checkpoint")
):
    
    try:

        print(f"Selected Directory: {selected_dir}")
        print(f"Epochs: {epochs}")
        print(f"Early Stopping: {early_stopping}")
        print(f"Best Model: {best_model}")
        print(f"Reduce LR on Plateau: {reduce_lr_on_plateau}")
        print(f"Checkpoint: {checkpoint}")
        

        # Update early_stopping and reduce_lr_on_plateau based on epochs
        if epochs <= 50:
            if early_stopping:
                print("Note: Early stopping will not be activated as epochs are 50 or less.")
                early_stopping = False
            if reduce_lr_on_plateau:
                print("Note: Reduce LR on Plateau will not be activated as epochs are 50 or less.")
                reduce_lr_on_plateau = False

        # Call the train_model function with all parameters
        epoch_metrics = await train_model(
            selected_dir=selected_dir,
            epochs=epochs,
            early_stopping=early_stopping,
            best_model=best_model,
            reduce_lr_on_plateau=reduce_lr_on_plateau,
            checkpoint=checkpoint
            
        )

        model_save_path = dire.models_path

        return {
            "message": "Model training completed successfully.",
            "model_save_path": model_save_path,
            "epoch_metrics": epoch_metrics 
            
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    


@router.websocket("/train_model_ws")
async def train_model_ws(websocket: WebSocket, selected_dir: str, epochs: int, early_stopping: bool = False, best_model: bool = False, reduce_lr_on_plateau: bool = False, checkpoint: bool = False):
    try:
        # Accept the WebSocket connection
        await websocket.accept()
        print(f"WebSocket connected. Starting training for directory: {selected_dir}")

        # Call the train_model function with WebSocket
        await train_model(
            selected_dir=selected_dir,
            epochs=epochs,
            early_stopping=early_stopping,
            best_model=best_model,
            reduce_lr_on_plateau=reduce_lr_on_plateau,
            checkpoint=checkpoint,
            websocket=websocket
        )

        print("Model training completed.")
    except Exception as e:
        print(f"An error occurred during model training: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        await websocket.close()
        print("WebSocket connection closed.")
    



    



