from dataclasses import dataclass

from pydantic import BaseModel


@dataclass
class BatchSettingsData:
    batch_erode: int
    batch_close: int


@dataclass
class ChipSettingsData:
    chip_noise_erode: int
    chip_dilate: int
    chip_erode: int
    crop_size: int


class Coordinates(BaseModel):
    norm_x_center: float
    norm_y_center: float


class ChipCoordinates(Coordinates):
    pass


class BatchCoordinates(Coordinates):
    norm_batch_width: float
    norm_batch_height: float


class SettingsCoordinates(BaseModel):
    coordinates: list[BatchCoordinates | ChipCoordinates]
