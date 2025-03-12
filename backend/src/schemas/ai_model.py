from dataclasses import dataclass

from constants.tf_model import ModelStatus


@dataclass
class DatasetInfo:
    count: int
    classes: list
    class_counts: dict


@dataclass
class EpochData:
    time: str
    epoch: str
    total_epoch: str
    accuracy: str
    loss: str
    val_accuracy: str
    val_loss: str
    learning_rate: str
    status: ModelStatus
