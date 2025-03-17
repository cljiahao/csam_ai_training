from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi import APIRouter

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.logic.sets_counter import get_eval_base_sets_data
from apis.v2.schemas.summary import EvalBaseSetsData
from db.session import get_db

router = APIRouter()


@router.get(
    "/eval_base_set_count",
    response_model=EvalBaseSetsData,
    summary="Return Eval and Base Sets count",
    operation_id="EvalBaseSetCount",
)
def eval_base_sets_count(
    db: Annotated[Session, Depends(get_db)],
):
    try:
        return get_eval_base_sets_data(db)
    except Exception as e:
        handle_exceptions(e)
