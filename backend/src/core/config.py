import os
import json
from pathlib import Path

from dotenv import load_dotenv

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings:
    PROJECT_NAME: str = "CSAM AI TRAINING"
    PROJECT_VERSION: str = "1.0.0"

    DBTYPE: str = os.getenv("DBTYPE")
    USER: str = os.getenv("USER")
    PASSWORD = os.getenv("PASSWORD")
    SERVER: str = os.getenv("SERVER", "localhost")
    PORT: str = os.getenv("PORT", 5432)  # default postgres port is 5432
    DB: str = os.getenv("DB", "tdd")
    DATABASE_URL = f"{DBTYPE}://{USER}:{PASSWORD}@{SERVER}:{PORT}/{DB}"

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
