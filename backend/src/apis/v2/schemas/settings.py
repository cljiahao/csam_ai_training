from dataclasses import dataclass

from schemas.chips_data import CoordsData


@dataclass
class ChipSettingsData(CoordsData):
    pass


@dataclass
class BatchSettingsData(CoordsData):
    norm_data_width: float
    norm_data_height: float
