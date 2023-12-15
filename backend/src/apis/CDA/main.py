import time


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
