from tensorflow import keras
from keras import callbacks as cb

from core.read_json import read_config, write_config


class TrainCallback(cb.Callback):
    def __init__(self, epochs):
        super().__init__()
        self.epochs = epochs

    def on_epoch_end(self, epoch, logs=None):
        train_set = read_config("./core/json/train.json")
        f_end_data = train_set["Frontend"]

        if f_end_data["status"] == "complete":
            f_end_data["epoch"] = 0

        f_end_data["status"] = "running"
        f_end_data["epoch"] += 1

        for key in logs.keys():
            f_end_data[key] = round(logs.get(key), 3)

        if self.epochs == f_end_data["epoch"]:
            f_end_data["status"] = "complete"

        train_set["Frontend"] = f_end_data
        write_config("./core/json/train.json", train_set)
