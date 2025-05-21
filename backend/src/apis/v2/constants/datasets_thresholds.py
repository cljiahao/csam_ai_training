from enum import IntEnum, StrEnum


class AIModelMode(StrEnum):
    TRAIN = "train"
    RETRAIN = "retrain"


class EvaluationDatasetsThresholds(IntEnum):
    MASS_PRO = 5
    PER_COLOR = 10
    THOUSANDS_SMALL = 800
    THOUSANDS_MED_AND_BIG = 100


class DatasetSummaryThresholds(IntEnum):
    MAX_DATASET = 30000
