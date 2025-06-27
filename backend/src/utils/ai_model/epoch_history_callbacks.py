import time
from tensorflow import keras
from keras import callbacks as cb

from constants.tensorflow_model import HyperParameters, ModelFiles, ModelStatus
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager

# TODO: pytest
class EpochHistory(cb.Callback):
    """A custom Keras Callback to record epoch-wise training metrics and time."""

    def __init__(self, is_train: bool = True) -> None:
        super().__init__()
        json_file = ModelFiles.TRAINING_JSON if is_train else ModelFiles.RETRAINING_JSON
        self.model_json_dir = dm.json_dir / json_file
        self.epoch_results = []
        self.start_time = 0.0
        self.status = ModelStatus.TRAINING if is_train else ModelStatus.RETRAINING
        self.final_status = ModelStatus.TRAINED if is_train else ModelStatus.RETRAINED

    # TODO: create on_train_start and put total_epoch, status and epoch_data instead of a list of dict
    def on_epoch_begin(self, epoch: int, logs: dict[str, any] = None) -> None:
        """Record the start time for each epoch.

        Args:
            epoch: The current epoch number (0-indexed).
            logs: Dictionary of logs.
        """
        self.start_time = time.perf_counter()

    def on_epoch_end(self, epoch: int, logs: dict[str, any] = None) -> None:
        """Append the epoch logs with time taken and write them to JSON.

        Args:
            epoch: The current epoch number (0-indexed).
            logs: Dictionary of logs containing training metrics.
        """
        end_time = time.perf_counter()
        time_taken = int(round(end_time - self.start_time))

        epoch_data = {
            "time": time_taken,
            "epoch": epoch + 1,
            "total_epoch": HyperParameters.EPOCHS,
            "status": self.status,
        }

        if logs:
            epoch_data.update({key: float(round(logs.get(key, 0), 3)) for key in logs})

        self.epoch_results.append(epoch_data)
        FileManager.write_json(self.model_json_dir, self.epoch_results)

    def on_train_end(self, logs: dict[str, any] = None) -> None:
        """Mark the last epoch's status as appropriate upon the completion of training.

        Args:
            logs: Dictionary of logs.
        """
        latest_epoch_data = FileManager.read_json(self.model_json_dir)

        if not latest_epoch_data:
            raise ValueError(f"No training data found in {self.model_json_dir}")

        latest_epoch_data[-1]["status"] = self.final_status
        FileManager.write_json(self.model_json_dir, latest_epoch_data)