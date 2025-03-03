import numpy as np
from dataclasses import dataclass
from cv2.typing import RotatedRect


@dataclass
class ContourInfo:
    contour: np.ndarray
    rect: RotatedRect
    area: float

    class Config:
        arbitrary_types_allowed = True


@dataclass
class ContourList:
    contours: list[ContourInfo]

    def __len__(self) -> int:
        return len(self.contours)

    def get_median_area(self) -> float:
        """Calculate the median area of the contours in the list."""
        if not self.contours:
            raise ValueError("No contours available to calculate median area.")
        contour_areas = np.array([contour_info.area for contour_info in self.contours])
        average_area = np.median(contour_areas)
        print(f"Average Chip Area is {average_area}")

        return average_area

    def get_max_area(self) -> float:
        """Calculate the largest area of the contours in the list."""
        if not self.contours:
            raise ValueError("No contours available to calculate largest area.")
        contour_areas = np.array([contour_info.area for contour_info in self.contours])
        largest_area = contour_areas.max()
        print(f"Largest Chip Area is {largest_area}")

        return largest_area

    def get_average_length(self) -> float:
        """Calculate the average length of the contours in the list."""
        if not self.contours:
            raise ValueError("No contours available to calculate average length.")
        longest_side_value = np.array(
            [max(contour_info.rect[1]) for contour_info in self.contours]
        )
        average_length = np.median(longest_side_value)
        print(f"Average Chip Length found is {average_length:0.2f}")

        return average_length
