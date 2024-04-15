import cv2
import time
import os
import uuid
import logging
from apis.utils.directory import dire

def cvWin(img):
    """
    Parameters
    ----------
    img : numpy array
        Image to mask out background
    """
    cv2.namedWindow("img", cv2.WINDOW_FREERATIO)
    cv2.imshow("img", img)
    cv2.waitKey(0)


def time_print(start, func_name) -> None:
    """
    Parameters
    ----------
    start : float
        Start time from previous recording
    func_name : string
        Description for previous recording
    """
    print(f"{func_name} took: {round(time.time()-start,2)} secs")

    return time.time()

def setup_logger(name, log_file, level=logging.INFO):
    """Sets up a logger with a file handler that includes a unique UUID in each log entry."""
    
    unique_id = uuid.uuid4()

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.FileHandler(os.path.join(dire.datasend_path, log_file))
        formatter = logging.Formatter(
            f'{unique_id},%(asctime)s,%(message)s', 
            datefmt='%Y/%m/%d %H:%M:00'  
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger