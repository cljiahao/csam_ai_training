import os
from fastapi import APIRouter

from apis.utils.directory import dire
from apis.utils.recursive import recursion

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


@router.get("/eval_folders")
def eval_folders():
    eval_info = {}
    pred_info = {}
    if os.path.exists(dire.eval_path):
        for eval_point in os.listdir(dire.eval_path):
            path = os.path.join(dire.eval_path, eval_point)
            type, key = eval_point.split("_", 1)
            if type.lower() == "c":
                for root, dirs, files in os.walk(path):
                    if len(dirs):
                        continue
                    path_list = root.split(key)[-1].split(os.sep)[1:]
                    path_list.insert(0, key)
                    if len(path_list) == 1:
                        eval_info[path_list[0]] = len(files)
                        pred_info[path_list[0]] = 0
                    else:
                        recursion(eval_info, path_list, len(files))
                        recursion(pred_info, path_list, 0)

            elif type.lower() == "p":
                for root, dirs, files in os.walk(path):
                    if len(dirs):
                        continue
                    last_fol = os.path.split(root)[-1]
                    if last_fol == "original":
                        continue
                    path_list = root.split(key)[-1].split(os.sep)[1:]
                    path_list.insert(0, key)
                    recursion(eval_info, path_list, 0)
                    recursion(pred_info, path_list, 0)

    return {"eval": eval_info, "pred": pred_info}
