from fastapi import APIRouter

from apis.CDA.main import aug_process
from core.read_json import write_config


router = APIRouter()


@router.post("/process_img")
def process_img(input: dict):
    # try:
    write_config("./core/json/trackbar.json", input["range"])
    aug_process(input["range"], input["entry"])
    alert = {
        "title": "Image Augmented",
        "text": "Confirm to Continue",
        "icon": "success",
        "confirmButtonText": "Confirm",
    }

    # except Exception as e:
    #     print(e)
    #     alert = {
    #         "title": "Image Failed to Augment!",
    #         "text": "Please Try Again",
    #         "icon": "error",
    #         "confirmButtonText": "Confirm",
    #     }
    return alert
