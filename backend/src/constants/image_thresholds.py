from enum import Enum, IntEnum, StrEnum


class ImageThreshold(Enum):
    """Enum for image processing thresholds."""

    BATCH_MULTIPLIER = 0.01
    CHECK_SINGLE_THRESHOLD = 10
    DENOISE_THRESHOLD = 50
    BACKGROUND_THRESHOLD = 130


class AugmentThreshold(IntEnum):
    """Enum for augmentation thresholds."""

    BASE_MULTIPLIER = 10
    SMALL_SIZE_THRESHOLD = 5
    BIG_SIZE_THRESHOLD = 40
    MAX_FILE_COUNT = 30000


class EvaluationThreshold(IntEnum):
    """Enum for evaluation thresholds."""

    MIN_MASS_PRO_SET = 5
    MIN_PER_COLORS_SET = 10
    MIN_SMALL_THOUSANDS_SET = 800
    MIN_MEDIUM_BIG_THOUSANDS_SET = 100


class EvalThousandsNames(StrEnum):
    """Enum for evaluation thousands names."""

    SMALL = "small"
    MEDIUM = "medium"
    BIG = "big"


class EvalColorsNames(StrEnum):
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
