from abc import ABC, abstractmethod

from cv2 import RotatedRect
import numpy as np


class MaskHandlerInterface(ABC):
    @abstractmethod
    def apply_morphology(self, batch_erode: int, batch_close: int) -> np.ndarray:
        pass


class ChipProcessorInterface(ABC):
    @abstractmethod
    def rotate_chips(
        self,
        border_image: np.ndarray,
        rect: RotatedRect,
        border_pad: int,
        crop_size: int,
    ) -> np.ndarray:
        pass
