from enum import StrEnum


class EvaluationSetsFolderName(StrEnum):
    EVALUATION = "evaluation"
    MASS_PRO = "mass_pro"
    COLORS = "colors"
    THOUSANDS = "thousands"


class MassProFolderNames(StrEnum):
    """Enum for evaluation mass pro names."""

    NG = "ng"
    TEMP = "temp"


class ColorsFolderNames(StrEnum):
    """Enum for evaluation color names."""

    BLACK_BIG = "black_big"
    BLUE_SMALL = "blue_small"
    BLUE_MEDIUM = "blue_medium"
    BLUE_BIG = "blue_big"
    CYAN_SMALL = "cyan_small"
    CYAN_MEDIUM = "cyan_medium"
    CYAN_BIG = "cyan_big"
    GREEN_SMALL = "green_small"
    GREEN_MEDIUM = "green_medium"
    GREEN_BIG = "green_big"
    LIME_SMALL = "lime_small"
    LIME_MEDIUM = "lime_medium"
    LIME_BIG = "lime_big"
    ORANGE_SMALL = "orange_small"
    ORANGE_MEDIUM = "orange_medium"
    ORANGE_BIG = "orange_big"
    YELLOW_SMALL = "yellow_small"
    YELLOW_MEDIUM = "yellow_medium"
    YELLOW_BIG = "yellow_big"


class ThousandsFolderNames(StrEnum):
    """Enum for evaluation thousands names."""

    SMALL = "small"
    MEDIUM = "medium"
    BIG = "big"


class BaseSetsFolderName(StrEnum):
    BASE = "base"
    NG = "ng"
    GOOD = "good"
    OTHERS = "others"
    DEFORM = "deform"


class ReTrainFolderName(StrEnum):
    RETRAIN = "retrain"
    NG = "ng"
    GOOD = "good"
    OTHERS = "others"


class ModelDatasetFolderNames(StrEnum):
    DATASET = "dataset"
    TRAIN = "train"
    VALIDATION = "validation"
