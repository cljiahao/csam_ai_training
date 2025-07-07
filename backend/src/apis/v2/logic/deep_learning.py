from datetime import datetime as dt
from pathlib import Path
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from apis.v2.components.defects_augmentation import augment_base_with_defects
from apis.v2.components.model_evaluation import (
    setup_evaluation_environment,
    start_evaluating,
)
from apis.v2.components.model_training import start_training
from apis.v2.components.model_retraining import start_retraining
from constants.folder_names import EvaluationSetsFolderName
from apis.v2.schemas.deep_learning import (
    EvaluationOutcome,
    TrainingEpochProgress,
    TrainingInitiated,
    Status,
)
from constants.tensorflow_model import ModelFiles, ModelStatus
from core.directory_manager import directory_manager as dm
from core.file_manager import FileManager
from db.services.image_settings import ImageSettingsService
from utils.debug import timer


@timer("Defects Augmentation")
def start_defects_augmentation(item: str) -> Status:
    """Initiates the process of augmenting base images with defect examples."""
    augment_base_with_defects(item)
    return Status(status=ModelStatus.AUGMENTED)


@timer("AI Model Training")
def ai_model_training(
    item: str, db: Session, background_tasks: BackgroundTasks
) -> TrainingInitiated:
    """Initiates AI model training in the background."""
    image_settings_service = ImageSettingsService(db)
    image_settings = image_settings_service.read_image_settings_not_empty(item)

    file_name = f"{dt.now().strftime('%Y%m%d_%H%M%S')}_{item}"

    background_tasks.add_task(start_training, item, image_settings.crop_size, file_name)

    return TrainingInitiated(status=ModelStatus.TRAINING, ai_model_name=file_name)


@timer("AI Model Retraining")
def ai_model_retraining(
    item: str, ai_model_name: str, db: Session, background_tasks: BackgroundTasks
) -> TrainingInitiated:
    """Initiates AI model retraining in the background."""

    image_settings_service = ImageSettingsService(db)
    image_settings = image_settings_service.read_image_settings_not_empty(item)

    model_stem = Path(ai_model_name).stem
    new_file_name = f"{model_stem}_retrained"

    background_tasks.add_task(
        start_retraining,
        item,
        image_settings.crop_size,
        model_stem,
        new_file_name
    )

    return TrainingInitiated(status=ModelStatus.RETRAINING, ai_model_name=new_file_name)


def get_current_epoch(is_train: bool) -> list[TrainingEpochProgress]:
    """Get the current epoch from the json file and return the results as a JSON object."""
    json_file = ModelFiles.TRAINING_JSON if is_train else ModelFiles.RETRAINING_JSON
    model_json_dir = dm.json_dir / json_file
    epoch_json_data = FileManager.read_json(model_json_dir)

    return [TrainingEpochProgress(**item) for item in epoch_json_data]


@timer("AI Model Evaluation")
def ai_model_evaluation(
    item: str, ai_model_name: str, db: Session
) -> EvaluationOutcome:
    """Initiates AI model evaluation on specified subdirectories."""
    image_settings_service = ImageSettingsService(db)
    image_settings = image_settings_service.read_image_settings_not_empty(item)
    input_size = image_settings.crop_size

    evaluation_dir = dm.images_dir / EvaluationSetsFolderName.EVALUATION / item
    colors_dir = evaluation_dir / EvaluationSetsFolderName.COLORS
    thousands_dir = evaluation_dir / EvaluationSetsFolderName.THOUSANDS
    mass_pro_dir = evaluation_dir / EvaluationSetsFolderName.MASS_PRO

    model, class_names = setup_evaluation_environment(item, ai_model_name)

    colors_eval_results = start_evaluating(
        colors_dir, input_size, model, class_names, None
    )
    thousands_eval_results = start_evaluating(
        thousands_dir, input_size, model, class_names, None
    )
    mass_pro_eval_results = start_evaluating(
        mass_pro_dir, input_size, model, class_names
    )
    evaluation_results = [
        colors_eval_results,
        thousands_eval_results,
        mass_pro_eval_results,
    ]

    return EvaluationOutcome(status=ModelStatus.EVALUATED, results=evaluation_results)


def get_all_model_names() -> list[dict[str, str]]:
    """Lists model filenames (excluding class label file extension) within subdirectories."""
    return [
        {
            "item": item_dir.name,
            "file_name": model_path.name,
        }
        for item_dir in dm.model_dir.iterdir()
        if item_dir.is_dir()
        for model_path in item_dir.iterdir()
        if model_path.is_file() and model_path.suffix != ModelFiles.LABEL_EXT
    ]


def delete_model_selected(item: str, ai_model_file_name: str) -> None:
    """Deletes the model file and its associated label file."""
    ai_model_name = Path(ai_model_file_name).stem
    model_path = dm.model_dir / item / ai_model_file_name
    label_path = dm.model_dir / item / f"{ai_model_name}{ModelFiles.LABEL_EXT}"

    for path in [model_path, label_path]:
        path.unlink()
