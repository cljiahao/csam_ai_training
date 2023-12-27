from fastapi import APIRouter

from core.read_json import read_config

router = APIRouter()


@router.get("/settings")
def get_settings():
    settings = read_config("./core/json/augment.json")
    return settings
