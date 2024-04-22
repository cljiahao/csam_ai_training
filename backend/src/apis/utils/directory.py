import os

from datetime import datetime as dt
from shutil import make_archive, rmtree


class Directory:
    src_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    base_path = os.path.dirname(src_path)

    conf_path = os.path.join(base_path, "conf")
    json_path = os.path.join(conf_path, "json")

    data_path = os.path.join(base_path, "data")
    image_path = os.path.join(data_path, "images")
    dataset_path = os.path.join(data_path, "dataset")
    eval_path = os.path.join(data_path, "evaluation")
    data_send_path = os.path.join(data_path, "datasend")
    models_path = os.path.join(data_path, "models")


dire = Directory


def zip_check_dataset(main_path, bypass):
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
    bp = "" if bypass else "_Aug"

    if len(fol_arr) == 0:
        if len(os.listdir(old_path)) > 0:
            last_old_version = sorted(
                os.listdir(old_path),
                key=lambda x: int(x.split("_")[0][1:]),
                reverse=True,
            )[0]
            lov_name = last_old_version.split("_")[0]
            new_v = f"V{int(lov_name[1:]) + 1}"
        else:
            new_v = f"V1"
    else:
        lastest_version = sorted(
            fol_arr, key=lambda x: int(x.split("_")[0][1:]), reverse=True
        )[0]
        last_name = lastest_version.split("_")[0]
        new_v = f"V{int(last_name[1:]) + 1}"

    new_version = f"{new_v}{bp}_{date}"

    return new_version
