import time

from apis.utils.directory import dire, zip_check_dataset


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


def evaluation():
    new_version = zip_check_dataset(dire.results_path)

    return
