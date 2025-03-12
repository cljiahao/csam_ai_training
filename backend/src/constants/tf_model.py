from enum import Enum


class ModelStatus(Enum):
    AUGMENT = "augment"
    AUGMENTED = "augmented"
    TRAINING = "training"
    TRAINED = "trained"
    EVALUATING = "evaluating"
    COMPLETED = "completed"


class ClassLabel(Enum):
    NG = "NG"
    G = "G"
    OTHERS = "Others"
    TEMP = "Temp"


class TFModel(Enum):
    BATCH_SIZE = 64
    EPOCHS = 10000
    SEED = 12345
    KER = (3, 3)
    KER2 = (1, 1)
