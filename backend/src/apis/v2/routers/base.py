from enum import StrEnum
from fastapi import APIRouter

from apis.v2.routers import image, model, settings, summary


class APITag(StrEnum):
    """Enum to define API tags for better organization and documentation."""

    IMAGE = "image"
    MODEL = "model"
    SETTINGS = "settings"
    SUMMARY = "summary"


router = APIRouter()

router.include_router(image.router, tags=[APITag.IMAGE], prefix="/image")
router.include_router(model.router, tags=[APITag.MODEL], prefix="/model")
router.include_router(settings.router, tags=[APITag.SETTINGS], prefix="/settings")
router.include_router(summary.router, tags=[APITag.SUMMARY], prefix="/summary")
