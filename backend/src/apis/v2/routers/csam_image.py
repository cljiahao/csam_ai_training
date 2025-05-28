import json
import os
import shutil
import tempfile
from fastapi import APIRouter, BackgroundTasks, Response, status, UploadFile
from fastapi import Depends, File, Form, Path
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import Annotated

from apis.v2.logic.csam_image import (
    prepare_datasets_for_retraining,
    prepare_datasets_for_training,
)
from apis.v2.schemas.common import ServerMode
from apis.v2.schemas.csam_image import FileDataBatchDirectory
from core.config import service_settings
from core.directory_manager import directory_manager as dm
from db.session import get_db

router = APIRouter()


def parse_form_data(
    item: Annotated[
        str, Form(description="Item Type", examples=[service_settings.TEST_ITEM])
    ],
    lot_no: Annotated[
        str,
        Form(
            description="Lot Number",
            pattern="[a-zA-Z0-9]{10}",
            examples=[service_settings.TEST_LOT_NO],
        ),
    ],
    defect_batch_directory: Annotated[
        str, Form(..., description="JSON string of FileDataBatchDirectory")
    ],
) -> dict[str, str | list[str]]:
    try:
        # Convert JSON string to Pydantic model
        defect_batch_directory_json = json.loads(defect_batch_directory)
        defect_batch_directory_model = FileDataBatchDirectory(
            **defect_batch_directory_json
        )
        defect_file_list = {
            data_file.file_name
            for defect_batch in defect_batch_directory_model.file_data_batches
            for data_file in defect_batch.defect_records
            if data_file.defect_mode.lower() != "temp"
        }
        return {
            "item": item,
            "lot_no": lot_no,
            "defect_file_list": defect_file_list,
        }
    except Exception as e:
        raise ValueError(f"Invalid JSON: {str(e)}")


def background_file_clean_up(
    item: str,
    lot_no: str,
    file_name: str,
    file_path: str,
    defect_batch_directory: FileDataBatchDirectory,
    is_ai: bool,
    db: Session,
) -> None:
    try:
        if is_ai:
            prepare_datasets_for_retraining(
                item, lot_no, file_name, file_path, defect_batch_directory, db
            )
        else:
            prepare_datasets_for_training(
                item, lot_no, file_name, file_path, defect_batch_directory, db
            )
    finally:
        os.remove(file_path)  # Clean up by deleting the temporary file


@router.post(
    "/process_image/{server_mode}",
    summary="Process User Judgement and Save Locally",
    operation_id="SaveUserJudgement",
    status_code=status.HTTP_204_NO_CONTENT,
)
def start_process_image(
    server_mode: Annotated[ServerMode, Path(description="Server Mode (CAI or CDC)")],
    data: Annotated[dict, Depends(parse_form_data)],
    file: Annotated[
        UploadFile,
        File(description="Upload image file ('.jpg','.png')"),
    ],
    db: Annotated[Session, Depends(get_db)],
    background_tasks: BackgroundTasks,
) -> Response:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        shutil.copyfileobj(file.file, tmp_file)
        tmp_path = tmp_file.name  # Store the file path

    is_ai = server_mode == ServerMode.CAI
    background_tasks.add_task(
        background_file_clean_up,
        data["item"],
        data["lot_no"],
        file.filename,
        tmp_path,
        data["defect_file_list"],
        is_ai,
        db,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/{src:path}",
    summary="Return image data",
    operation_id="ImageSource",
)
def get_image(
    src: Annotated[
        str,
        Path(
            description="Path to the image file relative to the image directory",
            pattern=".*\.(png|jpg)$",
        ),
    ],
) -> FileResponse:
    file_path = dm.images_dir / src
    if not file_path.exists():
        raise FileNotFoundError(f"Image file not found: {src}")
    return FileResponse(file_path)
