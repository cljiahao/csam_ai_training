import requests
from pathlib import Path

from core.config import service_settings
from core.directory_manager import directory_manager as dm
from core.logging import logger
from services.base import APIClient
from utils.debug import error_handler


API_INSTALL_MODEL_ENDPOINT = "/api/v2/upload/install_model"


@error_handler()
def post_model_files(item: str, ai_model_name: str) -> any:
    """Posts model files (label and model) to the AI server for installation."""
    file_name = Path(ai_model_name).stem
    label_file_path = dm.model_dir / item / f"{file_name}.txt"
    model_file_path = dm.model_dir / item / ai_model_name

    if not label_file_path.exists():
        raise FileNotFoundError(f"Label file not found: {label_file_path}")
    if not model_file_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_file_path}")

    file_path_list: dict[str, Path] = {
        "file_model_label": label_file_path,
        "file_model": model_file_path,
    }

    url = f"{API_INSTALL_MODEL_ENDPOINT}?item={item}"
    api_client = APIClient(service_settings.AI_SERVER_URL)
    result = api_client.post_files(url, file_path_list=file_path_list)

    logger.info(f"Successfully posted model files ({ai_model_name}) to {url}")

    return result
