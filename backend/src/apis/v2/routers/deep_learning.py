from fastapi import APIRouter, BackgroundTasks, Path, Response, status, HTTPException
from fastapi import Body, Depends, Query
from sqlalchemy.orm import Session
from typing import Annotated

from apis.v2.constants.datasets_thresholds import AIModelMode
from apis.v2.logic.deep_learning import (
    ai_model_evaluation,
    ai_model_training,
    ai_model_retraining,
    delete_model_selected,
    get_all_model_names,
    get_current_epoch,
    start_defects_augmentation,
)
from apis.v2.schemas.deep_learning import (
    TrainingEpochProgress,
    EvaluationOutcome,
    Status,
    TrainingInitiated,
)
from core.config import service_settings
from db.session import get_db
from services.server import post_model_files

router = APIRouter()


@router.post(
    "/augment_defects",
    response_model=Status,
    summary="Start Defects Augmentation Process",
    operation_id="AugmentDefects",
)
def augment_defects(
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
) -> Status:
    return start_defects_augmentation(item)


@router.post(
    "/train_model",
    response_model=TrainingInitiated,
    summary="Start Training a model with provided datasets",
    operation_id="TrainModel",
)
async def train_model(
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    db: Annotated[Session, Depends(get_db)],
    background_tasks: BackgroundTasks,
) -> TrainingInitiated:
    return ai_model_training(item, db, background_tasks)


@router.post(
    "/re_train_model",
    response_model=TrainingInitiated,
    summary="Continue training an existing model with provided datasets",
    operation_id="ReTrainModel",
)
async def retrain_model(
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    ai_model_name: Annotated[str, Query(description="Name of the model to retrain")],
    db: Annotated[Session, Depends(get_db)],
    background_tasks: BackgroundTasks,
) -> TrainingInitiated:
    return ai_model_retraining(item, ai_model_name, db, background_tasks)


@router.get(
    "/current_epoch/{ai_model_mode}",
    response_model=list[TrainingEpochProgress],
    summary="Get the current training epoch status",
    operation_id="CurrentEpoch",
)
def current_epoch(
    ai_model_mode: Annotated[
        AIModelMode, Path(description="AI Model Mode (Train or ReTrain)")
    ],
) -> list[TrainingEpochProgress]:
    is_train = ai_model_mode == AIModelMode.TRAIN
    return get_current_epoch(is_train)


@router.post(
    "/evaluate_model",
    response_model=EvaluationOutcome,
    summary="Evaluate trained model and return evaluated results",
    operation_id="EvaluateModel",
)
def evaluate_model(
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    ai_model_name: Annotated[str, Body(description="Name of the model", embed=True)],
    db: Annotated[Session, Depends(get_db)],
) -> EvaluationOutcome:
    return ai_model_evaluation(item, ai_model_name, db)


@router.get(
    "/all_model_names",
    response_model=list[dict[str, str]],
    summary="Get all model names stored in model folder",
    operation_id="AllModelNames",
)
def all_model_names() -> list[dict[str, str]]:
    return get_all_model_names()


@router.post(
    "/install_model",
    summary="Install selected model remotely into Server (Production)",
    operation_id="InstallModel",
    status_code=status.HTTP_204_NO_CONTENT,
)
def install_model_in_server(
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    ai_model_name: Annotated[str, Query(description="Name of the model", embed=True)],
) -> Response:
    post_model_files(item, ai_model_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete(
    "/delete_model",
    summary="Delete selected model from Training folder",
    operation_id="DeleteModel",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_model_in_training(
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    ai_model_file_name: Annotated[
        str, Query(description="Name of the model file", embed=True)
    ],
) -> Response:
    delete_model_selected(item, ai_model_file_name)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
