from dataclasses import dataclass
from enum import Enum


class BGRColors(Enum):
    BACKGROUND = (192, 192, 192)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (255, 0, 0)
    CYAN = (255, 255, 0)
    GREEN = (0, 255, 0)
    LIME = (0, 255, 192)
    ORANGE = (0, 191, 255)
    RED = (0, 0, 255)
    YELLOW = (0, 255, 255)


@dataclass(frozen=True)
class ColorInfo:
    name: str
    bgr: tuple[int, int, int]


class CSAMcolor(Enum):
    BLACK = ColorInfo(name="Black", bgr=BGRColors.BLACK.value)
    BLUE = ColorInfo(name="Blue", bgr=BGRColors.BLUE.value)
    CYAN = ColorInfo(name="Cyan", bgr=BGRColors.CYAN.value)
    GREEN = ColorInfo(name="Green", bgr=BGRColors.GREEN.value)
    LIME = ColorInfo(name="Lime", bgr=BGRColors.LIME.value)
    ORANGE = ColorInfo(name="Orange", bgr=BGRColors.ORANGE.value)
    YELLOW = ColorInfo(name="Yellow", bgr=BGRColors.YELLOW.value)
