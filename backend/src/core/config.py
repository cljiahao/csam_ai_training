import os
import json

from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())


class Settings:
    PROJECT_NAME: str = "CSAM AI TRAINING"
    PROJECT_VERSION: str = "1.0.0"

    CORS: list = json.loads(os.getenv("CORS"))
    PRASS_URL: str = os.getenv("PRASS_URL")
    LOT_COL: str = os.getenv("LOT_NO_COL")
    ITEM_COL: str = os.getenv("CHIP_TYPE_COL")
    ITEM: str = os.getenv("CHIPTYPE")

    REALTIMEDB: str = os.getenv("REALTIMEDB")
    TABLEID_AUG: str = os.getenv("TABLEID_AUG")
    TABLEID_TRAIN: str = os.getenv("TABLEID_TRAIN")
    TABLEID_EVAL: str = os.getenv("TABLEID_EVAL")

    # For Augment
    G_TYPES: list = ["G", "Good", "g", "good"]
    BASE_TYPES: list = ["Base", "base"]

    # For training
    IMAGE_SIZE: list = [54, 54]
    INPUT_SHAPE: tuple = (54, 54, 3)
    BATCH_SIZE: int = 64
    SEED: int = 12345
    KER: tuple = (3, 3)
    SKER: tuple = (1, 1)


settings = Settings()
