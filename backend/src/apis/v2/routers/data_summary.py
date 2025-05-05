from typing import Annotated
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from apis.v2.logic.data_summary import get_eval_base_sets_data
from apis.v2.schemas.data_summary import EvalBaseSetsData
from db.session import get_db

router = APIRouter()


@router.get(
    "/",
    response_model=EvalBaseSetsData,
    summary="Get Eval and Base Datasets count",
    operation_id="EvalBaseSetCount",
)
def eval_base_sets_count(
    db: Annotated[Session, Depends(get_db)],
):
    return get_eval_base_sets_data(db)
