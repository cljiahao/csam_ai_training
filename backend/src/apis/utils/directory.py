import os

from datetime import datetime as dt
from shutil import make_archive, rmtree


class Directory:
    base_path = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    )
    image_path = os.path.join(base_path, "images")
    dataset_path = os.path.join(base_path, "dataset")
    eval_path = os.path.join(base_path, "evaluation")
    results_path = os.path.join(base_path, "results")
    models_path = os.path.join(base_path, "models")
    old_path = os.path.join(dataset_path, "old")


dire = Directory


def zip_check_dataset(main_path):
    """Zipping function"""
    old_path = os.path.join(main_path, "old")
    if not os.path.exists(old_path):
        os.makedirs(old_path)
    fol_arr = [fol for fol in os.listdir(main_path) if fol != "old"]

    if len(fol_arr) > 9:
        to_be_zipped = sorted(fol_arr, key=lambda x: int(x.split("_")[0][1:]))[0]
        make_archive(
            os.path.join(old_path, to_be_zipped),
            "zip",
            main_path,
            to_be_zipped,
        )
        rmtree(os.path.join(main_path, to_be_zipped))

    date = dt.now().strftime("%d%m%y")

    if len(fol_arr) == 0:
        if len(os.listdir(old_path)) > 0:
            last_old_version = sorted(
                os.listdir(old_path),
                key=lambda x: int(x.split("_")[0][1:]),
                reverse=True,
            )[0]
            lov_name = last_old_version.split("_")[0]
            new_version = f"V{int(lov_name[1:]) + 1}_{date}"
        else:
            new_version = f"V1_{date}"
    else:
        lastest_version = sorted(
            fol_arr, key=lambda x: int(x.split("_")[0][1:]), reverse=True
        )[0]
        last_name = lastest_version.split("_")[0]
        new_version = f"V{int(last_name[1:]) + 1}_{date}"

    return new_version
