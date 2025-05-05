from typing import Annotated
from fastapi import APIRouter, UploadFile
from fastapi import Depends, File, Path, Query
from sqlalchemy.orm import Session

from apis.v2.constants.csam_thresholds import SettingsMode
from apis.v2.logic.image_settings import auto_settings_finder
from apis.v2.schemas.image_settings import SettingsCoordinates
from core.config import service_settings
from db.services.image_settings import ImageSettingsService
from db.session import get_db

router = APIRouter()


@router.get(
    "/",
    summary="Return image settings found in database",
    operation_id="ImageSettings",
)
def get_image_settings(
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    db: Annotated[Session, Depends(get_db)],
):
    image_settings_service = ImageSettingsService(db)
    image_settings = image_settings_service.read_image_settings(item)
    return image_settings


@router.post(
    "/{settings_mode}",
    response_model=SettingsCoordinates,
    summary="Run Auto Settings Finder for either Batch or Chip",
    operation_id="SettingsFinder",
)
def run_settings_finder(
    settings_mode: Annotated[
        SettingsMode, Path(description="Settings Mode (Batch or Chip)")
    ],
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    target_count: Annotated[int, Query(description="Target Count")],
    file: Annotated[UploadFile, File(description="Upload image file ('.jpg','.png')")],
    db: Annotated[Session, Depends(get_db)],
) -> SettingsCoordinates:
    is_batch = settings_mode == SettingsMode.BATCH
    return auto_settings_finder(item, target_count, file, db, is_batch)
