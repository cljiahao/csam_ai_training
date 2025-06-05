import numpy as np
from pathlib import Path
from sklearn.metrics import confusion_matrix
from tensorflow import data, keras
from keras import models

from apis.v2.schemas.deep_learning import ConfusionMatrixResults, EvaluationResult
from constants.tensorflow_model import ModelFiles
from core.directory_manager import directory_manager as dm
from utils.ai_model.tensorflow_model import TensorflowModel


def start_evaluating(
    directory: Path,
    input_size: int,
    model: models.Sequential,
    class_names: dict[str, str],
    labels: str = "inferred",
) -> EvaluationResult:
    """Evaluates a trained AI model on multiple directories of image data."""

    eval_dataset, file_paths = TensorflowModel.prepare_dataset(
        directory, input_size, labels
    )

    true_labels, predicted_labels = run_model_evaluation(model, eval_dataset)
    cm_results, outflow_indexes, fake_ng_indexes = create_confusion_matrix(
        true_labels, predicted_labels, list(class_names.keys())
    )

    outflow_images = file_paths[outflow_indexes]
    fake_ng_images = file_paths[fake_ng_indexes]

    return EvaluationResult(
        mode=directory.name,
        total_count=len(file_paths),
        cm_results=cm_results,
        outflows=outflow_images,
        fake_ng=fake_ng_images,
    )


def setup_evaluation_environment(
    item: str, ai_model_name: str
) -> tuple[models.Sequential, dict[str, str]]:
    """Sets up the necessary environments for evaluation."""
    item_model_dir = dm.model_dir / item
    ai_model_path = item_model_dir / f"{ai_model_name}{ModelFiles.H5_MODEL_EXT}"
    txt_path = item_model_dir / f"{ai_model_name}{ModelFiles.LABEL_EXT}"

    model = TensorflowModel.load_model(ai_model_path)
    class_names = TensorflowModel.read_class_txt(txt_path)

    return model, class_names


def run_model_evaluation(
    model: models.Sequential, dataset: data.Dataset
) -> tuple[np.ndarray, np.ndarray]:
    """Runs the model evaluation on a given TensorFlow dataset."""
    true_labels = []
    for items in dataset:
        if isinstance(items, tuple) and len(items) == 2:
            image_batch, label_batch = items
            true_labels.extend(label_batch.numpy())
        else:
            image_batch = items
            true_labels.extend([1] * len(image_batch))
    pred_batch = model.predict(dataset, batch_size=256, verbose=0)
    predicted_classes = np.argmax(pred_batch, axis=-1)

    return np.array(true_labels), np.array(predicted_classes)


def create_confusion_matrix(
    true_labels: np.ndarray, predicted_labels: np.ndarray, class_names: list[int]
) -> tuple[ConfusionMatrixResults, np.ndarray, np.ndarray]:
    """Creates a confusion matrix and related metrics for binary classification."""
    cm = confusion_matrix(true_labels, predicted_labels, labels=class_names)
    TP = np.diag(cm)
    FN = cm.sum(axis=1) - np.diag(cm)
    FP = cm.sum(axis=0) - np.diag(cm)
    TN = cm.sum() - (FP + FN + TP)

    cm_results = ConfusionMatrixResults(
        true_pos=int(TP[1]),
        false_neg=int(FN[1]),
        false_pos=int(FP[1]),
        true_neg=int(TN[1]),
    )

    outflow_indexes = (true_labels == 1) & (predicted_labels == 0)
    fake_ng_indexes = (true_labels == 0) & (predicted_labels == 1)

    return cm_results, outflow_indexes, fake_ng_indexes
