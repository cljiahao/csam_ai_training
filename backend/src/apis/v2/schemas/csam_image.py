import numpy as np
from uuid import UUID
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional


class DefectInfo(BaseModel):
    label_mode: str
    defect_size: Optional[str]
    defect_color: Optional[str]


class LabeledImageData(DefectInfo):
    file_name: str
    image_data: np.ndarray

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CoordsData(BaseModel):
    norm_x_center: float
    norm_y_center: float

    @field_validator("norm_x_center", "norm_y_center")
    def validate_coordinates(cls, v: float) -> float:
        if not (0.0 <= v <= 1.0):
            raise ValueError("Coordinates must be between 0.0 and 1.0.")
        return v


class DefectData(CoordsData):
    file_name: str
    defect_mode: str


class FileDataBatch(BaseModel):
    batch_no: str
    data_files: list[DefectData]


class FileDataBatchDirectory(BaseModel):
    unique_id: UUID
    directory: str
    file_data_batches: list[FileDataBatch] = []
