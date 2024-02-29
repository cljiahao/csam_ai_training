import asyncio
from tensorflow import keras
from keras import optimizers, losses

from apis.utils.directory import dire, zip_check_dataset
from apis.CMT.training.architecture import callback, create_new_model
from apis.CMT.training.dataset import create_image_dataset


async def training(sel_fold, epochs, sel_cb):
    train_ds, train_info, validation_ds, validation_info = create_image_dataset(
        sel_fold
    )

    model = create_new_model(train_info["class_counts"])
    model.compile(
        optimizer=optimizers.Adam(learning_rate=0.001),
        loss=losses.SparseCategoricalCrossentropy(),
        metrics=["accuracy"],
    )
    # Does not return anything
    # model.summary()

    cb_arr = callback(sel_cb, epochs)

    for i in range(epochs):
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


def evaluation():

    return
