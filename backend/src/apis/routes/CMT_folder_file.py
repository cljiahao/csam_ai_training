import os
from fastapi import APIRouter
from pydantic import BaseModel

from apis.utils.directory import dire
from apis.utils.recursive import recursion

router = APIRouter()


@router.get("/item_type")
def get_item_type():
    return os.listdir(dire.dataset_path)


@router.get("/all_models")
def get_all_models():
    model_list = {}
    for folder in os.listdir(dire.models_path):
        fold_path = os.path.join(dire.models_path, folder)
        model_list[folder] = [
            x.split(".")[0] for x in os.listdir(fold_path) if x.split(".")[-1] != "txt"
        ]

    return model_list


class directory(BaseModel):
    item: str
    folder: str


@router.post("/ds_file_count")
def ds_file_count(fol_dir: directory):
    folder_path = os.path.join(dire.dataset_path, fol_dir.item, fol_dir.folder)
    folder_dict = {}
    for root, dir, files in os.walk(folder_path):
        if len(files):
            recursion(
                folder_dict,
                root.split(fol_dir.folder)[-1].split(os.sep)[1:],
                len(files),
            )
    return folder_dict


class item_type(BaseModel):
    item: str


@router.post("/ds_folders")
def ds_folders(item_type: item_type):
    path = os.path.join(dire.dataset_path, item_type.item)
    folder_list = os.listdir(path)
    if "old" in folder_list:
        folder_list.remove("old")
    return folder_list


@router.post("/eval_folders")
def eval_folders(item_type: item_type):
    eval_info = {}
    pred_info = {}
    base_path = os.path.join(dire.eval_path, item_type.item)
    if os.path.exists(base_path):
        for eval_point in os.listdir(base_path):
            path = os.path.join(base_path, eval_point)
            type, key = eval_point.split("_", 1)
            if type.lower() == "c":
                for root, dirs, files in os.walk(path):
                    if len(dirs):
                        continue
                    path_list = root.split(key)[-1].split(os.sep)[1:]
                    path_list.insert(0, key)
                    if len(path_list) == 1:
                        eval_info[path_list[0]] = {
                            "res": {"counter": len(files), "outflow": []}
                        }
                        pred_info[path_list[0]] = {"res": {"counter": 0, "outflow": []}}
                    else:
                        recursion(
                            eval_info,
                            path_list,
                            {"res": {"counter": len(files), "outflow": []}},
                        )
                        recursion(
                            pred_info, path_list, {"res": {"counter": 0, "outflow": []}}
                        )

            elif type.lower() == "p":
                for root, dirs, files in os.walk(path):
                    if len(dirs):
                        continue
                    last_fol = os.path.split(root)[-1]
                    if last_fol == "original":
                        continue
                    path_list = root.split(key)[-1].split(os.sep)[1:]
                    path_list.insert(0, key)
                    recursion(
                        eval_info, path_list, {"res": {"counter": 0, "outflow": []}}
                    )
                    recursion(
                        pred_info, path_list, {"res": {"counter": 0, "outflow": []}}
                    )

    return {"actual": eval_info, "predict": pred_info}
