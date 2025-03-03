def get_norm_coordinates(
    coords: list[int, int], size: list[int, int], border_pad: int = 0
):

    x, y = coords
    height, width = size

    norm_x = round((x - border_pad) / (width - border_pad * 2), 6)
    norm_y = round((y - border_pad) / (height - border_pad * 2), 6)
    return norm_x, norm_y
