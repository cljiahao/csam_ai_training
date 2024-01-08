from ast import Dict
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from apis.CMT.training.train_model import train_model
from apis.utils.directory import dire
import json
from typing import List, Dict



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

@router.post("/train_model/")
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