from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import Depends, File, Path, Query
from fastapi import APIRouter, UploadFile

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.logic.auto_settings_finder import auto_settings_finder
from apis.v2.schemas.base import SettingsMode
from apis.v2.schemas.settings import FileDataLists
from db.services.image_settings import ImageSettingsService
from db.session import get_db

router = APIRouter()


@router.get(
    "/image",
    summary="Return image settings found in database",
    operation_id="ImageSettings",
)
def get_image_settings(
    item: Annotated[
        str, Query(description="Item Type", examples=["GCM32ER71E106KA59_+B55-E02GJ"])
    ],
    db: Annotated[Session, Depends(get_db)],
):
    image_settings_service = ImageSettingsService(db)
    image_settings = image_settings_service.read_image_settings(item)
    return image_settings


@router.post(
    "/{settings_mode}",
    response_model=FileDataLists,
    summary="Return Example based on example provided",
    operation_id="SettingsFinder",
)
def run_settings_finder(
    settings_mode: Annotated[SettingsMode, Path(description="Settings Mode")],
    item: Annotated[str, Query(description="Item Type")],
    target_count: Annotated[int, Query(description="Target Count")],
    file: Annotated[UploadFile, File(description="Upload image file ('.jpg','.png')")],
    db: Annotated[Session, Depends(get_db)],
):
    try:
        is_batch = settings_mode == SettingsMode.batch
        return auto_settings_finder(item, target_count, file, db, is_batch)
    except Exception as e:
        handle_exceptions(e)
