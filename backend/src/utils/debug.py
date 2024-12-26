import cv2
import time
import numpy as np
from datetime import timedelta

from core.logging import logger


def cvWin(image: np.ndarray, name: str = "image") -> None:
    """Display an image using OpenCV for debugging purposes.

    Args:
        image : np.ndarray
            The image to be displayed.
        name : str
            The name of the window. Defaults to "image".
    """

    cv2.namedWindow(name, cv2.WINDOW_FREERATIO)
    cv2.imshow(name, image)
    if cv2.waitKey(0) & 0xFF == ord("q"):
        cv2.destroyAllWindows()


def timer(print_message=""):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = timedelta(seconds=end_time - start_time)
            if print_message:
                logger.info(f"{print_message} took: {elapsed_time}", stacklevel=2)
            else:
                logger.info(f"Total time taken: {elapsed_time}", stacklevel=2)
            return result

        return wrapper

    return decorator
