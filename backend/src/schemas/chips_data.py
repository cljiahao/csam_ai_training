import numpy as np
from dataclasses import dataclass


@dataclass
class ImageData:
    file_name: str
    rotated_image: np.ndarray
    label_mode: str
    defect_color: str
    defect_size: str


@dataclass
class CoordsData:
    norm_x_center: float
    norm_y_center: float


@dataclass
class DefectData(CoordsData):
    file_name: str
    defect_mode: str


@dataclass
class FileDataBatch:
    batch_no: str
    data_files: list[DefectData]
