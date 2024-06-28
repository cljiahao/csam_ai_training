import os
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi import APIRouter

from apis.utils.directory import dire
from core.read_write import read_json, write_json


router = APIRouter()


class Parameters(BaseModel):
    name: str
    range: dict


@router.post("/save_parameters")
def random_img(parameters: Parameters):

    data = {parameters.name: parameters.range}
    path = os.path.join(dire.json_path, "settings.json")
    write_json(path, data)

    return FileResponse(
        path,
        filename=os.path.basename(path),
    )


class RangeName(BaseModel):
    name: str


@router.post("/get_range")
def random_img(range_name: RangeName):
    range = {}
    data = read_json(os.path.join(dire.json_path, "settings.json"))
    if range_name.name in data:
        range = data[range_name.name]

    return range
