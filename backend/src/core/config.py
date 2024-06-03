import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())


class Settings:
    PROJECT_NAME: str = "CSAM AI TRAINING"
    PROJECT_VERSION: str = "1.0.0"

    FASTAPI_ROOT: str = f"{os.getenv('FASTAPI_ROOT')}/"
    CORS: list = [f"http://{os.getenv('PC_NAME')}:{os.getenv('NGINX_PORT')}"]

    LOCAL_DB_PATH: str = os.getenv("LOCAL_DB_PATH")
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
