import time
from tensorflow import keras
from keras import callbacks as cb

from constants.tf_model import TFModel
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager


class EpochHistory(cb.Callback):

    def __init__(self) -> None:
        super().__init__()
        self.model_json_dir = dm.config_dir / "json" / "training.json"
        self.epoch_results = []

    def on_epoch_begin(self, epoch, logs=None) -> None:
        """Record the start time for each epoch."""
        self.start_time = time.perf_counter()

    def on_epoch_end(self, epoch, logs=None) -> None:
        """Append the epoch logs and write them to JSON."""
        end_time = time.perf_counter()
        time_taken = round(end_time - self.start_time)

        epoch_data = {
            "time": time_taken,
            "epoch": epoch + 1,
            "total_epoch": TFModel.EPOCHS.value,
            "status": "training",
        }

        if logs:
            epoch_data.update({key: round(logs.get(key, 0.0), 3) for key in logs})

        self.epoch_results.append(epoch_data)
        FileManager.write_json(self.model_json_dir, self.epoch_results)

    def on_train_end(self, logs=None) -> None:
        """Mark the last epoch's status as 'trained'."""
        latest_epoch_data = FileManager.read_json(self.model_json_dir)

        if not latest_epoch_data:
            raise ValueError(f"No training data found in {self.model_json_dir}")

        latest_epoch_data[-1]["status"] = "trained"
        FileManager.write_json(self.model_json_dir, latest_epoch_data)
