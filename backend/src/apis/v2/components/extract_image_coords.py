from apis.v2.helpers.math_calculations import get_norm_coordinates
from apis.v2.schemas.settings import BatchSettingsData, ChipSettingsData
from schemas.contours import ContourList
from utils.debug import timer


@timer("Extract Batch Coords")
def extract_batch_coords(
    image_size: tuple[int, int], contour_info_list: ContourList
) -> list[BatchSettingsData]:
    """Extract batch coordinates from contour information."""
    return _extract_coords(image_size, contour_info_list, is_batch=True)


@timer("Extract Chips Coords")
def extract_chip_coords(
    image_size: tuple[int, int], contour_info_list: ContourList
) -> list[ChipSettingsData]:
    """Extract chip coordinates from contour information."""
    return _extract_coords(image_size, contour_info_list, is_batch=False)


def _extract_coords(
    image_size: tuple[int, int],
    contour_info_list: ContourList,
    is_batch: bool = False,
) -> list:
    """Helper function to extract normalized coordinates for batch or chip data."""
    data_list = []

    for contour_info in contour_info_list.contours:
        coords, (temp_width, temp_height), _ = contour_info.rect
        norm_x_center, norm_y_center = get_norm_coordinates(coords, image_size)

        if is_batch:
            # Logic specific to batch settings
            data_size = (
                (temp_width, temp_height)
                if temp_width < temp_height
                else (temp_height, temp_width)
            )
            norm_data_width, norm_data_height = get_norm_coordinates(
                data_size, image_size
            )

            data_list.append(
                BatchSettingsData(
                    norm_x_center=norm_x_center,
                    norm_y_center=norm_y_center,
                    norm_data_width=norm_data_width,
                    norm_data_height=norm_data_height,
                )
            )
        else:
            # Logic specific to chip settings
            data_list.append(
                ChipSettingsData(
                    norm_x_center=norm_x_center,
                    norm_y_center=norm_y_center,
                )
            )

    return data_list
