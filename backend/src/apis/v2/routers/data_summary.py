from typing import Annotated
from fastapi import APIRouter, Path
from fastapi import Depends
from sqlalchemy.orm import Session

from apis.v2.constants.datasets_thresholds import AIModelMode
from apis.v2.logic.data_summary import get_datasets_summary, get_eval_base_sets_data
from apis.v2.schemas.data_summary import DatasetsSummary, TrainSetsSummary
from db.session import get_db

router = APIRouter()


@router.get(
    "/{ai_model_mode}",
    response_model=(TrainSetsSummary | DatasetsSummary),
    summary="Get Eval and Base Datasets count",
    operation_id="EvalBaseSetCount",
)
def data_summary(
    ai_model_mode: Annotated[
        AIModelMode, Path(description="AI Model Mode (Train or ReTrain)")
    ],
    db: Annotated[Session, Depends(get_db)],
) -> TrainSetsSummary | DatasetsSummary:
    is_train = ai_model_mode == AIModelMode.TRAIN
    return get_datasets_summary(db, is_train)
