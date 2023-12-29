import os

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
    # TODO: Reset version and delete old folder if takes up too much space
    # TODO: Check if there is more than 1 version in folder (Due to user intervention)

    old_path = os.path.join(main_path, "old")
    if not os.path.exists(old_path):
        os.makedirs(old_path)
    fol_arr = [fol for fol in os.listdir(main_path) if fol != "old"]

    # Archiving / zipping old versions to make way for new version
    # TODO: Speed up processing using threading or asyncio
    if len(fol_arr) > 0:
        latest_version = fol_arr[0]  # Assuming only 1 version in the folder
        make_archive(
            os.path.join(old_path, latest_version),
            "zip",
            main_path,
            latest_version,
        )
        rmtree(os.path.join(main_path, latest_version))
        new_version = f"V{int(latest_version[1:]) + 1}"
    elif len(os.listdir(old_path)) > 0:
        last_old_version = sorted(os.listdir(old_path), reverse=True)[0]
        lov_name = last_old_version.split(".")[0]
        new_version = f"V{int(lov_name[1:]) + 1}"
    else:
        new_version = "V1"

    return new_version
