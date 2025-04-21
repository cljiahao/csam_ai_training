import cv2
import numpy as np
from pathlib import Path

from apis.v2.helpers.processor.eval_processor import EvalProcessor
from constants.folder_names import FolderNames
from constants.tf_model import ClassLabel
from core.directory_manager import directory_manager as dm
from utils.ai_model.tf_model import TensorflowModel
from utils.debug import timer
from utils.image_process.image_manager import ImageManager


@timer("Loaded Other Evaluation Files")
def load_images_from_directory(
    directory: Path,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Loads and processes images from a directory, returning image arrays and labels."""
    rgb_images = []
    labels = []
    image_paths = []

    for subdir in directory.iterdir():
        if subdir.is_dir():
            for file_path in subdir.iterdir():
                if file_path.is_file():
                    image = cv2.cvtColor(
                        ImageManager.path_to_image(file_path), cv2.COLOR_BGR2RGB
                    )
                    rgb_images.append(image)
                    labels.append(1)
                    image_paths.append(str(file_path.relative_to(dm.images_dir)))

    return np.array(rgb_images), np.array(labels), np.array(image_paths)


@timer("Loaded Mass Production Files")
def load_mass_production_files(mass_pro_dir: Path) -> dict[str, list]:
    """Loads mass production files, grouped by their stem name."""
    rgb_images = []
    labels = []
    image_paths = []

    for mass_pro_folder in mass_pro_dir.iterdir():
        if mass_pro_folder.is_dir():
            ng_files = list((mass_pro_folder / ClassLabel.NG.value).iterdir())
            for temp_file_path in (mass_pro_folder / ClassLabel.TEMP.value).iterdir():
                image = cv2.cvtColor(
                    ImageManager.path_to_image(temp_file_path), cv2.COLOR_BGR2RGB
                )
                rgb_images.append(image)
                labels.append(1 if temp_file_path in ng_files else 0)
                image_paths.append(str(temp_file_path.relative_to(dm.images_dir)))

    return np.array(rgb_images), np.array(labels), np.array(image_paths)


@timer("Evaluated Model")
def evaluate_model(item: str, ai_model_name: str) -> list[dict]:
    """Evaluates the model using images from various directories (colors, thousands, mass_pro)."""
    eval_processor = EvalProcessor(item)
    tf_model = TensorflowModel(item, ai_model_name)

    directories = [
        (FolderNames.COLORS.value, eval_processor.colors_dir),
        (FolderNames.THOUSANDS.value, eval_processor.thousands_dir),
        (FolderNames.MASS_PRO.value, eval_processor.mass_pro_dir),
    ]

    results = []

    for mode, directory in directories:
        files, labels, file_paths = (
            load_images_from_directory(directory)
            if mode != FolderNames.MASS_PRO.value
            else load_mass_production_files(directory)
        )

        # Initialize the model and evaluate
        cm_result, outflow_index = tf_model.start_evaluating(files, labels)

        # Get the outflow images (incorrectly classified images)
        outflow_images = file_paths[outflow_index]

        # Append results
        results.append(
            {
                "mode": mode.title(),
                "total_count": len(file_paths),
                "cm_results": cm_result,
                "outflows": list(outflow_images),
            }
        )

    return results
