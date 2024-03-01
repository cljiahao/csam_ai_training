import os

from apis.utils.recursive import recursion


def process(path, key, results, error, model, labels):
    for root, dirs, files in os.walk(path):
        if len(dirs):
            continue
        if len(files):
            last_fol = os.path.split(root)[-1]
            if last_fol == "original":
                continue
            path_list = root.split(key)[-1].split(os.sep)[1:]
            path_list.insert(0, key)
            recursion(results, path_list)


def img_process():
    return


def predict():
    return
