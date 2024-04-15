import os
import numpy as np
from tensorflow import keras
from keras import preprocessing as pp
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from apis.utils.recursive import recursion
from apis.utils.misc import setup_logger

logger = setup_logger('evaluation_logger', 'evaluation_results.csv')

def folder_path(path):
    p = Path(path)
    try:
        evaluation_index = [i for i, part in enumerate(p.parts) if part == 'evaluation'][0]
        return p.parts[evaluation_index + 2] 
    except (IndexError, ValueError):
        return p.name  

def evaluate(path, key, results, model, labels):
    for root, dirs, files in os.walk(path):
        if len(dirs):
            continue
        path_list = root.split(key)[-1].split(os.sep)[1:]
        path_list.insert(0, key)
        if len(files):
            if any(not file.endswith(".png") for file in files):
                print("error")
            else:
                if len(path_list) == 1:
                    results[path_list[0]] = predict(root, model, labels)
                else:
                    recursion(results, path_list, predict(root, model, labels))
        else:
            if len(path_list) == 1:
                results[path_list[0]] = {"res": {"counter": 0, "outflow": []}}
            else:
                recursion(results, path_list, {"res": {"counter": 0, "outflow": []}})

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

    res = {"res": {"counter": 0, "outflow": []}}

    for i, file_path in enumerate(pred_path):
        if labels[pred[i]] != os.path.split(root)[-1]:
            res["res"]["outflow"].append(
                {
                    "image_path": file_path,
                    "name": os.path.split(file_path)[-1],
                    "label": os.path.split(root)[-1],
                    "pred": labels[pred[i]],
                }
            )
        else:
            res["res"]["counter"] += 1

    folder_name = folder_path(root)
    logger.info(f"{folder_name},{os.path.split(root)[-1]},{len(pred_path)},{res['res']['counter']},{len(res['res']['outflow'])}")

    return res
