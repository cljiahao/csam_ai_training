from typing import Annotated
from fastapi import APIRouter, UploadFile
from fastapi import Depends, File, Path, Query
from sqlalchemy.orm import Session

from apis.v2.constants.csam_thresholds import SettingsMode
from apis.v2.logic.image_settings import (
    auto_settings_finder,
    get_image_settings_by_item,
)
from apis.v2.schemas.image_settings import SettingsCoordinates
from core.config import service_settings
from db.session import get_db

router = APIRouter()


@router.get(
    "",
    response_model=dict[str, int],
    summary="Return image settings found in database",
    operation_id="ImageSettings",
)
def image_settings(
    item: Annotated[
        str, Query(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    db: Annotated[Session, Depends(get_db)],
) -> dict[str, int]:
    return get_image_settings_by_item(item, db)


@router.post(
    "/{settings_mode}",
    response_model=SettingsCoordinates,
    summary="Run Auto Settings Finder for either Batch or Chip",
    operation_id="SettingsFinder",
)
def settings_finder(
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
