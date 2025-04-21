from enum import StrEnum
from dataclasses import dataclass


class ModelStatus(StrEnum):
    """Enum for model status."""

    AUGMENT = "augment"
    AUGMENTED = "augmented"
    TRAINING = "training"
    TRAINED = "trained"
    EVALUATING = "evaluating"
    COMPLETED = "completed"


class ClassLabel(StrEnum):
    """Enum for class labels."""

    NG = "NG"
    G = "G"
    OTHERS = "Others"
    TEMP = "Temp"


@dataclass(frozen=True)
class TFModelParams:
    """Dataclass for TensorFlow model parameters."""

    BATCH_SIZE: int = 64
    EPOCHS: int = 10000
    SEED: int = 12345
    KER: tuple[int, int] = (3, 3)
    KER2: tuple[int, int] = (1, 1)
