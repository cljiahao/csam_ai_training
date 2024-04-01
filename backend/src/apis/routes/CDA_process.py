from fastapi import APIRouter
from pydantic import BaseModel

from apis.CDA.main import aug_process
from core.read_json import write_config


router = APIRouter()


class Response(BaseModel):
    range: dict
    item: str
    entry: dict
    bypass: bool


@router.post("/process_img")
def process_img(input: Response):

    try:
        write_config("./core/json/trackbar.json", input.range)
        aug_process(input)
        title = (
            "Bypass Completed,\n Dataset Created"
            if input.bypass
            else "Image Augmented,\n Dataset Created"
        )
        alert = {
            "title": title,
            "text": "Confirm to Continue",
            "icon": "success",
            "confirmButtonText": "Confirm",
        }
    except Exception as e:
        print(e)
        alert = {
            "title": "Image Failed to Augment!",
            "text": f"{e}",
            "icon": "error",
            "confirmButtonText": "Confirm",
        }

    return alert
