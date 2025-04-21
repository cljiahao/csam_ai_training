from enum import StrEnum


class FolderNames(StrEnum):
    """Enum for folder names."""

    BASE = "base"
    EVAL = "eval"
    RETRAIN = "retrain"
    DATASET = "dataset"
    TRAIN = "train"
    VALIDATION = "validation"
    MASS_PRO = "mass_pro"
    THOUSANDS = "thousands"
    COLORS = "colors"
