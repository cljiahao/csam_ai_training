import os
from fastapi import APIRouter

from apis.utils.directory import dire
from backend.src.apis.utils.recursive import recursion

router = APIRouter()

# TODO: Add Pydantic BaseModel for Post methods


@router.post("/ds_file_count")
def ds_file_count(folder: dict):
    folder_path = os.path.join(dire.dataset_path, folder["name"])
    folder_dict = {}
    for root, dir, files in os.walk(folder_path):
        if len(files):
            recursion(
                folder_dict,
                root.split(folder["name"])[-1].split(os.sep)[1:],
                len(files),
            )
    return folder_dict


@router.get("/ds_folders")
def ds_folders():
    folder_list = os.listdir(dire.dataset_path)
    if "old" in folder_list:
        folder_list.remove("old")
    return folder_list


# TODO Change for loop into recursion


@router.get("/eval_folders")
def eval_folders():
    eval_info = {}
    pred_info = {}
    if os.path.exists(dire.eval_path):
        for eval_point in os.listdir(dire.eval_path):
            path = os.path.join(dire.eval_path, eval_point)
            type, key = eval_point.split("_", 1)
            eval_info[key] = {}
            pred_info[key] = {}
            if type.lower() == "c":
                for root, dirs, files in os.walk(path):
                    if len(dirs) == 0:
                        last_fol = os.path.split(root)[-1]
                        if last_fol == eval_point:
                            eval_info[key] = len(files)
                            pred_info[key] = 0
                        else:
                            eval_info[key][last_fol] = len(files)
                            pred_info[key][last_fol] = 0

            elif type.lower() == "p":
                for lot_plate in os.listdir(path):
                    eval_info[key][lot_plate] = {}
                    pred_info[key][lot_plate] = {}
                    inner_path = os.path.join(path, lot_plate)
                    for root, dirs, files in os.walk(inner_path):
                        if len(dirs) == 0:
                            last_fol = os.path.split(root)[-1]
                            if last_fol == "original":
                                continue
                            eval_info[key][lot_plate][last_fol] = len(files)
                            pred_info[key][lot_plate][last_fol] = 0

    return {"eval": eval_info, "pred": pred_info}
