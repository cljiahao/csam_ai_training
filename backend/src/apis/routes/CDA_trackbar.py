import os
from fastapi import APIRouter

from apis.utils.directory import dire
from core.read_write import read_json, write_json


router = APIRouter()


@router.get("/get_trackbar")
def get_trackbar():
    trackbar_set = read_json(os.path.join(dire.json_path, "trackbar.json"))
    return trackbar_set


@router.post("/set_trackbar")
def set_trackbar(range: dict):
    try:
        write_json(os.path.join(dire.json_path, "trackbar.json"), range)
        alert = {
            "title": "Range Settings Saved",
            "text": "Confirm to Continue",
            "icon": "success",
            "confirmButtonText": "Confirm",
        }
    except:
        alert = {
            "title": "Range Failed to Save!",
            "text": "Please Try Again",
            "icon": "error",
            "confirmButtonText": "Confirm",
        }
    return alert
