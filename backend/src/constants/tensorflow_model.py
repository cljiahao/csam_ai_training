from enum import Enum, IntEnum, StrEnum


class DatasetModes(StrEnum):
    NG = "NG"
    G = "G"


class ModelFiles(StrEnum):
    LABEL_EXT = ".txt"
    MODEL_EXT = ".h5"
    TRAINING_JSON = "training.json"


class ModelStatus(StrEnum):
    AUGMENTED = "augmented"
    TRAINING = "training"
    TRAINED = "trained"
    EVALUATING = "evaluating"
    EVALUATED = "evaluated"
    COMPLETED = "completed"


class HyperParameters(IntEnum):
    BATCH_SIZE: int = 64
    EPOCHS: int = 10000
    SEED: int = 12345
