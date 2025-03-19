from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Body
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime as dt

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.logic.ai_evaluation import evaluate_model
from apis.v2.logic.ai_training import pre_process_dataset
from apis.v2.logic.defects_augmentation import defects_augmentation
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager
from db.session import get_db
from services.train import post_model_files
from utils.ai_training.tf_model import TensorflowModel


router = APIRouter()


@router.post(
    "/start_augment",
    summary="Start defect augmentation process",
    operation_id="Augment",
)
def start_defect_augment(
    item: Annotated[str, Query(description="Item Type")],
):
    try:
        defects_augmentation(item)
        return {"status": "augmented"}
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "/start_train",
    summary="Start training a model with the provided dataset",
    operation_id="TrainModel",
)
async def start_train_model(
    item: Annotated[str, Query(description="Item Type")],
    db: Annotated[Session, Depends(get_db)],
    background_tasks: BackgroundTasks,
):
    try:
        model_json_dir = dm.json_dir / "training.json"
        FileManager.write_json(model_json_dir, [])

        file_name = f"{dt.now().strftime('%Y%m%d_%H%M%S')}_{item}"
        input_size, output_size, train_ds, validation_ds = pre_process_dataset(
            file_name, item, db
        )

        tf_model = TensorflowModel(item, file_name)
        background_tasks.add_task(
            tf_model.start_training,
            input_size,
            output_size,
            train_ds,
            validation_ds,
        )
        return {"status": "training", "ai_model_name": file_name}
    except Exception as e:
        handle_exceptions(e)


@router.get(
    "/get_epoch",
    summary="Get the current training epoch status",
    operation_id="CurrentEpoch",
)
def current_epoch():
    model_json_dir = dm.config_dir / "json" / "training.json"
    return FileManager.read_json(model_json_dir)


@router.post(
    "/start_evaluate",
    summary="Evaluate the model and return results based on the example provided",
    operation_id="EvaluateModel",
)
def start_evaluate_model(
    item: Annotated[str, Query(description="Item Type")],
    ai_model_name: Annotated[str, Body(description="Name of the model", embed=True)],
):
    try:
        evaluate_results = evaluate_model(item, ai_model_name)
        return {"status": "evaluated", "results": evaluate_results}

    except Exception as e:
        handle_exceptions(e)


@router.get(
    "/model_names",
    summary="Get all model names stored in model folder.",
    operation_id="AllModelNames",
)
def get_all_model_names():
    try:
        return {
            item_dir.stem: [
                model_path.name
                for model_path in item_dir.iterdir()
                if model_path.is_file() and model_path.suffix != ".txt"
            ]
            for item_dir in dm.model_dir.iterdir()
            if item_dir.is_dir()
        }
    except Exception as e:
        handle_exceptions(e)


@router.post(
    "/install_model",
    summary="Post model selected to be install in Server (Production).",
    operation_id="InstallModel",
)
def install_model_in_server(
    item: Annotated[
        str, Query(description="Item Type", examples=["GCM32ER71E106KA59_+B55-E02GJ"])
    ],
    file_name: Annotated[str, Query(description="Model File Name")],
):
    try:
        return post_model_files(item, file_name)
    except Exception as e:
        handle_exceptions(e)
