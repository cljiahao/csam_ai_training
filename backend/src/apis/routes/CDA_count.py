import os
import random
from fastapi import APIRouter
from fastapi.responses import FileResponse

from apis.utils.directory import dire
from apis.CDA.main import get_files


router = APIRouter()


@router.get("/count_rand")
def count_rand():
    files = get_files(False)

    file_count = {}
    for fol in os.listdir(dire.image_path):
        file_count[fol] = {}
        fol_dict = {k: v for k, v in files.items() if fol in k}
        key, arr = random.sample(sorted(fol_dict.items()), 1)[0]
        file_name = random.sample(arr, 1)[0]
        file_count[fol]["file_path"] = f"{key}/{file_name}"
        file_count[fol]["count"] = sum(
            [len(files[a]) for a in files.keys() if fol in a]
        )

    return {"file_count": file_count}
