import os
import asyncio
from tensorflow import keras
from keras import optimizers, losses, models

from apis.utils.directory import dire, zip_check_dataset
from apis.CMT.training.architecture import callback, create_new_model
from apis.CMT.training.dataset import create_image_dataset
from apis.CMT.evaluate.evaluate import evaluate
from apis.CMT.evaluate.process import process


async def training(sel):
    # TODO: Check if files / folders exists
    train_ds, train_info, validation_ds, validation_info = create_image_dataset(
        sel.item, sel.folder
    )

    if sel.model != "":
        folder, name = sel.model.split("/")
        model_path = os.path.join(dire.models_path, folder, f"{name}.h5")
        model = models.load_model(model_path)
    else:
        model = create_new_model(train_info["class_counts"])
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),
        loss=losses.SparseCategoricalCrossentropy(),
        metrics=["accuracy"],
    )
    # Does not return anything
    # model.summary()

    cb_arr = callback(sel.callbacks, sel.epochs)

    for i in range(sel.epochs):
        model.fit(
            train_ds,
            validation_data=validation_ds,
            epochs=1,
            verbose=1,
            callbacks=cb_arr,
        )
        await asyncio.sleep(1)

    # TODO Save Model, Figure out what naming convention
    # TODO Save Label txt file for evaluation
    # TODO Call evaluation after training


def evaluation(item, model, labels):
    results = {}
    error = {"files": [], "exe": []}

    base_path = os.path.join(dire.eval_path, item)
    if os.path.exists(base_path):
        for eval_point in os.listdir(base_path):
            path = os.path.join(base_path, eval_point)
            type, key = eval_point.split("_", 1)
            if type.lower() == "c":
                evaluate(path, key, results, error, model, labels)
            elif type.lower() == "p":
                process(path, key, results, error, model, labels)

    return results
