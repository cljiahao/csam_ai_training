import os
from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter()


@router.get("/get_image/{url:path}")
def get_image(url: str):
    url = "/" + url
    if not os.path.exists(url):
        raise Exception(f"File at {url} not found")
    return FileResponse(url)
