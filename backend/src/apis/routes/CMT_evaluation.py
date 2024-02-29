import os
from fastapi import APIRouter

from apis.utils.directory import dire


router = APIRouter()


@router.post("/evaluation_folders")
def evaluation_folders():
    return
