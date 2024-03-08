import os
from fastapi import APIRouter
from fastapi.responses import FileResponse

from apis.utils.directory import dire


router = APIRouter()


@router.get("/get_image/{src:path}")
def get_image(src: str):
    file_path = os.path.join(dire.image_path, src)
    return FileResponse(file_path)
