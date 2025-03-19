import requests
from pathlib import Path

from core.config import service_settings
from core.directory_manager import directory_manager as dm
from services.base import APIClient


def post_model_files(item, ai_model_name: str):
    api_client = APIClient(service_settings.AI_SERVER_URL)
    try:
        file_name = Path(ai_model_name).stem
        file_path_list = {
            "file_model_label": dm.model_dir / item / f"{file_name}.txt",
            "file_model": dm.model_dir / item / f"{ai_model_name}",
        }

        result = api_client.post_files(
            f"/api/v2/upload/install_model?item={item}", file_path_list=file_path_list
        )
        return result
    except requests.RequestException as e:
        raise Exception(f"Failed to post model files: {e}")
