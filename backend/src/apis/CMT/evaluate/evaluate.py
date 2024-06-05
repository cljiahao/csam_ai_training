import os
import numpy as np
from tensorflow import keras
from keras import preprocessing as pp
from concurrent.futures import ThreadPoolExecutor

from apis.utils.recursive import recursion


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
        label = os.path.split(root)[-1]
        if labels[pred[i]] != label:
            res["res"]["outflow"].append(
                {
                    "image_path": file_path,
                    "name": os.path.split(file_path)[-1],
                    "label": label,
                    "pred": labels[pred[i]],
                }
            )
        else:
            res["res"]["counter"] += 1

    return res
