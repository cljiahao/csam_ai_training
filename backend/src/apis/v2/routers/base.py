from enum import Enum
from fastapi import APIRouter

from apis.v2.routers import image, model, settings


class APITag(str, Enum):
    """Enum to define API tags for better organization and documentation."""

    SETTINGS = "settings"
    MODEL = "model"
    IMAGE = "image"


router = APIRouter()

router.include_router(image.router, tags=[APITag.IMAGE], prefix="/image")
router.include_router(model.router, tags=[APITag.MODEL], prefix="/model")
router.include_router(settings.router, tags=[APITag.SETTINGS], prefix="/settings")
