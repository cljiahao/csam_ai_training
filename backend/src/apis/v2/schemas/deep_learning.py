from pydantic import BaseModel

from constants.tensorflow_model import ModelStatus


class Status(BaseModel):
    status: ModelStatus


class TrainingInitiated(Status):
    ai_model_name: str


class TrainingEpochProgress(Status):
    time: int
    epoch: int
    total_epoch: int
    accuracy: float
    loss: float
    val_accuracy: float
    val_loss: float


class ConfusionMatrixResults(BaseModel):
    true_pos: int
    false_neg: int
    false_pos: int
    true_neg: int


class EvaluationResult(BaseModel):
    mode: str
    total_count: int
    cm_results: ConfusionMatrixResults
    outflows: list[str]
    fake_ng: list[str]


class EvaluationOutcome(Status):
    results: list[EvaluationResult]
