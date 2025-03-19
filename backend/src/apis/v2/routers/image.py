import json
from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Path, UploadFile
from fastapi import File, Form, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from apis.v2.helpers.HTTPExceptions import handle_exceptions
from apis.v2.logic.eval_base_sets_creation import eval_base_image_sets_creation
from apis.v2.schemas.files import FileDataBatchDirectory
from core.directory_manager import directory_manager as dm
from db.session import get_db

router = APIRouter()


def parse_form_data(
    item: Annotated[
        str, Form(description="Item Type", examples=["GCM32ER71E106KA59_+B55-E02GJ"])
    ],
    lot_no: Annotated[
        str,
        Form(
            description="Lot Number",
            pattern="[a-zA-Z0-9]{10}",
            examples=["1234567890"],
        ),
    ],
    defect_batch_directory: Annotated[
        str, Form(..., description="JSON string of FileDataBatchDirectory")
    ],
):
    try:
        # Convert JSON string to Pydantic model
        defect_batch_directory = json.loads(defect_batch_directory)
        defect_batch_directory = FileDataBatchDirectory(**defect_batch_directory)

        # Return all extracted data
        return {
            "item": item,
            "lot_no": lot_no,
            "defect_batch_directory": defect_batch_directory,
        }
    except Exception as e:
        raise ValueError(f"Invalid JSON: {str(e)}")


@router.post(
    "/process_image",
    summary="Update local database with new user input",
    operation_id="SaveLocal",
)
def start_defect_augment(
    data: Annotated[dict, Depends(parse_form_data)],
    file: Annotated[
        UploadFile,
        File(description="Upload image file ('.jpg','.png')"),
    ],
    db: Annotated[Session, Depends(get_db)],
    background_tasks: BackgroundTasks,
):
    try:
        item = data["item"]
        lot_no = data["lot_no"]
        defect_batch_directory = data["defect_batch_directory"]

        background_tasks.add_task(
            eval_base_image_sets_creation,
            item,
            lot_no,
            file,
            defect_batch_directory,
            db,
        )
        return True
    except Exception as e:
        handle_exceptions(e)


@router.get(
    "/{src:path}",
    summary="Return image data",
)
def get_image(
    src: Annotated[
        str,
        Path(
            description="Path to the image file relative to the image directory",
            pattern=".*\.(png|jpg)$",
        ),
    ],
):
    try:
        file_path = dm.images_dir / src

        if not file_path.exists():
            raise FileNotFoundError(f"Image file not found: {src}")

        return FileResponse(file_path)
    except Exception as e:
        handle_exceptions(e)
