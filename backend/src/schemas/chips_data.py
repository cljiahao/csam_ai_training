import numpy as np
from dataclasses import dataclass


@dataclass
class ImageData:
    file_name: str
    rotated_image: np.ndarray
    label_mode: str
    defect_color: str
    defect_size: str
