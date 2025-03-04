from enum import Enum


class ImageThreshold(Enum):
    BATCH_MULTIPLIER = 0.01
    CHECK_SINGLE_THRESHOLD = 10
    DENOISE_THRESHOLD = 50
    BACKGROUND_THRESHOLD = 130


class EvaluationThreshold(Enum):
    MIN_MASS_PRO_SET = 3
    MIN_PER_COLOR_SET = 10
    MIN_SMALL_THOUSAND_SET = 800
    MIN_MEDIUM_BIG_THOUSAND_SET = 100


class EvalThousandNames(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    BIG = "big"


class EvalColorNames(Enum):
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
