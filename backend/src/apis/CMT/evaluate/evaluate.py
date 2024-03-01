import os
import numpy as np
from tensorflow import keras
from keras import preprocessing as pp
from concurrent.futures import ThreadPoolExecutor

from apis.utils.directory import dire
from backend.src.apis.utils.recursive import recursion


def evaluate(model, labels):

    results = {}
    error = {"files": [], "exe": []}

    if os.path.exists(dire.eval_path):
        for eval_point in os.listdir(dire.eval_path):
            path = os.path.join(dire.eval_path, eval_point)
            type, key = eval_point.split("_", 1)
            if type.lower() == "c":
                for root, dirs, files in os.walk(path):
                    path_list = root.split(eval_point)[-1].split(os.sep)[1:]
                    path_list.insert(0, eval_point)
                    if len(dirs):
                        continue
                    if len(files):
                        if any(not file.endswith(".png") for file in files):
                            error["exe"].append("_".join(path_list))
                        else:
                            recursion(results, path_list, predict(root, model, labels))
                            print(results)
                    else:
                        error["files"].append("_".join(path_list))

            # elif type.lower() == "p":
            #     for lot_plate in os.listdir(path):
            #         results[key][lot_plate] = {}
            #         inner_path = os.path.join(path, lot_plate)
            #         for root, dirs, files in os.walk(inner_path):
            #             if len(dirs) == 0:
            #                 last_fol = os.path.split(root)[-1]
            #                 if last_fol == "original":
            #                     continue
            #                 results[key][lot_plate][last_fol] = len(files)

    return results


def predict(root, model, labels):

    pred_img = pp.image_dataset_from_directory(
        root,
        label_mode=None,
        shuffle=False,
        batch_size=32,
        image_size=(54, 54),
        seed=12345,
    )
    pred_path = pred_img.file_paths
    pred = np.argmax(model.predict(pred_img), axis=1)

    arr = []

    for i, file_path in enumerate(pred_path):
        arr.append(
            {
                "image_path": file_path,
                "name": os.path.split(file_path)[-1],
                "label": os.path.split(root)[-1],
                "pred": labels[pred[i]],
            }
        )

    return arr
