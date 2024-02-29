import os
import numpy as np
import tensorflow.keras.models as Model

from shutil import copyfile
from concurrent.futures import ThreadPoolExecutor
from tensorflow.keras.preprocessing import image_dataset_from_directory

from apis.utils.directory import dire


def evaluate(model):
    for fol in os.listdir(dire.eval_path):
        fol_path = os.path.join(dire.eval_path, fol)

        with ThreadPoolExecutor(10) as exe:
            _ = [
                exe.submit(process_in_fol, model, fol, fol_path, in_fol)
                for in_fol in os.listdir(fol_path)
            ]

    return


def load_model(modelname):
    model = Model.load_model(os.path.join(dire.models_path, modelname))
    return model


def process_in_fol(model, fol, fol_path, in_fol):
    in_fol_path = os.path.join(fol_path, in_fol)

    if any(not file.endswith(".png") for file in os.listdir(in_fol_path)):
        raise Exception("Files / folders other than .png extension found")

    results_path = os.path.join(dire.results_path, fol, in_fol)
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    pred, pred_path = predict(model, in_fol_path)
    copy_false(os.listdir(in_fol_path), results_path, pred, pred_path)


def predict(model, in_fol_path):
    pred_img = image_dataset_from_directory(
        os.listdir(in_fol_path),
        label_mode=None,
        shuffle=False,
        batch_size=32,
        image_size=(54, 54),
        seed=12345,
        verbose=0,
    )
    pred_path = pred_img.file_paths
    pred = np.argmax(model.predict(pred_img), axis=1)

    return pred, pred_path


def copy_false(fol_arr, results_path, pred, pred_path):
    for i, p in enumerate(pred):
        if fol_arr[p] not in pred_path.split("//"):
            copyfile(
                pred_path[i],
                os.path.join(
                    results_path,
                ),
            )
