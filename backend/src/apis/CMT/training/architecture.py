from tensorflow import keras
from keras import layers, models, callbacks as cb

from apis.CMT.training.custom_cb import TrainCallback
from core.config import settings


# TODO: Future to make this dynamic (drag and drop?)
def create_new_model(out):
    input_shape = settings.INPUT_SHAPE
    seed = settings.SEED
    ker = settings.KER
    sker = settings.SKER

    model = models.Sequential(
        [
            layers.Rescaling(1.0 / 255, input_shape=input_shape),
            layers.RandomFlip("horizontal_and_vertical", seed=seed),
            layers.Conv2D(16, kernel_size=ker, activation="relu", padding="same"),
            layers.Conv2D(32, kernel_size=sker, activation="relu", padding="same"),
            layers.MaxPool2D(2, 2),
            layers.Conv2D(64, kernel_size=ker, activation="relu", padding="same"),
            layers.Conv2D(128, kernel_size=sker, activation="relu", padding="same"),
            layers.MaxPool2D(3, 2),
            layers.Conv2D(256, kernel_size=ker, activation="relu", padding="same"),
            layers.Conv2D(512, kernel_size=sker, activation="relu", padding="same"),
            layers.AveragePooling2D(3),
            layers.Flatten(),
            layers.Dropout(0.3),
            layers.Dense(out, activation="softmax"),
        ]
    )

    return model


def callback(selected_cb, epochs):
    cb_dict = {
        "early": cb.EarlyStopping(
            monitor="val_loss", patience=7, verbose=1, mode="min"
        ),
        "reducelr": cb.ReduceLROnPlateau(
            monitor="val_loss", factor=0.2, patience=3, min_lr=0.00001, verbose=1
        ),
        # "best": cb.ModelCheckpoint(
        #     best_modelpath, monitor="val_loss", save_best_only=True, verbose=1
        # ),
        # "check": cb.ModelCheckpoint(checkpoint_path, save_freq="epoch", verbose=1),
    }

    # tensorboard = cb.TensorBoard(
    #     log_dir="logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S"), histogram_freq=1
    # )

    cb_arr = [TrainCallback(epochs)]
    for key, value in selected_cb.items():
        if value:
            cb_arr.append(cb_dict[key.lower()])

    return cb_arr
