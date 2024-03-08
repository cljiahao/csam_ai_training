import os
import numpy as np

from apis.utils.recursive import recursion
from apis.CMT.evaluate.batch_process import mask
from apis.CMT.evaluate.chip_process import chips
from apis.CMT.evaluate.image_process import create_border_img


def process(path, item, key, results, model, labels):
    for root, dirs, files in os.walk(path):
        if len(dirs):
            pred_dict = []
            if "original" in dirs:
                ori_path = os.path.join(root, "original")
                file_paths = os.listdir(ori_path)
                if len(file_paths):
                    file_path = os.path.join(ori_path, file_paths[0])
                    pred_dict = img_process(file_path, item, model, labels)
            continue
        path_list = root.split(key)[-1].split(os.sep)[1:]
        path_list.insert(0, key)
        if len(files):
            if len(pred_dict) and os.path.split(root)[-1] != "original":
                recursion(results, path_list, compare(root, pred_dict))
        else:
            print(len(files))
            print(path_list)
            recursion(results, path_list, {"res": {"counter": 0, "outflow": []}})


def compare(root, pred_dict):

    file_paths = [os.path.join(root, file_path) for file_path in os.listdir(root)]

    res = {"res": {"counter": 0, "outflow": []}}

    for file_path in file_paths:
        file_name = os.path.split(file_path)[-1]
        pred_type = pred_dict[file_name] if file_name in pred_dict.keys() else "G"
        if pred_type != os.path.split(root)[-1]:
            res["res"]["outflow"].append(
                {
                    "image_path": file_path,
                    "name": file_name,
                    "label": os.path.split(root)[-1],
                    "pred": pred_type,
                }
            )
        else:
            res["res"]["counter"] += 1

    return res


def img_process(path, item, model, labels):
    border_img, gray, img_shape = create_border_img(path)
    batch_data = mask(gray, img_shape, item)
    no_of_chips, temp_dict, ng_dict = chips(border_img, gray, batch_data, "CAI", item)
    pred_dict = predict(temp_dict, model, labels)
    ng_dict = ng_dict.fromkeys(ng_dict, "Others")
    pred_dict.update(ng_dict)

    return pred_dict


def predict(pred_dict, model, labels):

    pred_arr = np.array(list(pred_dict.values()))
    pred_res = np.argmax(model.predict(pred_arr, batch_size=256, verbose=2), axis=1)

    for i, key in enumerate(list(pred_dict.keys())):
        if labels[pred_res[i]] in ["G", "g", "good", "Good"]:
            del pred_dict[key]
        else:
            pred_dict[key] = labels[pred_res[i]]

    return pred_dict
