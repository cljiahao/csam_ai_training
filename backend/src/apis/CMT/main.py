import os
import asyncio
from tensorflow import keras
from keras import optimizers, losses, models

from apis.utils.directory import dire
from apis.CMT.training.architecture import callback, create_new_model
from apis.CMT.evaluate.evaluate import evaluate
from apis.CMT.evaluate.process import process
from core.read_write import read_json, write_json


async def training(sel, file_name, train_ds, train_info, validation_ds):

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
        if sel.epochs == i + 1:
            model_path = os.path.join(
                dire.models_path,
                "temp",
                f"{file_name}.h5",
            )
            model.save(model_path)

        await asyncio.sleep(1)


def evaluation(item, model, labels):
    results = {}

    base_path = os.path.join(dire.eval_path, item)
    if os.path.exists(base_path):
        for eval_point in os.listdir(base_path):
            path = os.path.join(base_path, eval_point)
            type, key = eval_point.split("_", 1)
            if type.lower() == "c":
                evaluate(path, key, results, model, labels)
            elif type.lower() == "p":
                process(path, item, key, results, model, labels)

    train_set = read_json(os.path.join(dire.json_path, "train.json"))
    f_end_data = train_set["Frontend"]
    f_end_data["status"] = "complete"
    write_json(os.path.join(dire.json_path, "train.json"), train_set)

    return results
