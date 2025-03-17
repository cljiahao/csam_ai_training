import numpy as np
from tensorflow import keras
from sklearn.metrics import confusion_matrix
from keras import layers, models, optimizers, losses, callbacks as cb

from constants.tf_model import TFModel
from core.directory_manager import directory_manager as dm
from utils.ai_training.custom_callbacks import EpochHistory


class TensorflowModel:
    """A class to handle building, training, and evaluating TensorFlow models."""

    def __init__(self, ai_model_name: str) -> None:
        self.ai_model_name = ai_model_name
        self.model = None

    def _load_model(self) -> models.Sequential:
        """Loads a saved Keras model from disk."""
        model_path = dm.model_dir / f"{self.ai_model_name}.h5"
        if not model_path.exists():
            raise FileNotFoundError(
                f"{self.ai_model_name}.h5 not found in {dm.model_dir}"
            )
        self.model = models.load_model(model_path)
        return self.model

    def _build_model(self, input_size: int, output_size: int) -> models.Sequential:
        """Builds and compiles a CNN model based on predefined architecture."""
        ker = TFModel.KER.value
        ker2 = TFModel.KER2.value
        input_shape = (input_size, input_size, 3)

        model = models.Sequential(
            [
                layers.Input(shape=input_shape),
                layers.Rescaling(1.0 / 255),
                layers.RandomFlip("horizontal_and_vertical", seed=TFModel.SEED.value),
                layers.Conv2D(16, kernel_size=ker, activation="relu", padding="same"),
                layers.Conv2D(32, kernel_size=ker2, activation="relu", padding="same"),
                layers.MaxPool2D(2, 2),
                layers.Conv2D(64, kernel_size=ker, activation="relu", padding="same"),
                layers.Conv2D(128, kernel_size=ker2, activation="relu", padding="same"),
                layers.MaxPool2D(3, 2),
                layers.Conv2D(256, kernel_size=ker, activation="relu", padding="same"),
                layers.Conv2D(512, kernel_size=ker2, activation="relu", padding="same"),
                layers.AveragePooling2D(3),
                layers.Flatten(),
                layers.Dropout(0.3),
                layers.Dense(output_size, activation="softmax"),
            ]
        )

        model.compile(
            optimizer=optimizers.Adam(learning_rate=0.001),
            loss=losses.SparseCategoricalCrossentropy(),
            metrics=["accuracy"],
        )

        return model

    def _create_callbacks(self) -> list[cb.Callback]:
        """Creates a list of training callbacks."""
        early_stopping = cb.EarlyStopping(
            monitor="val_loss", patience=7, verbose=1, mode="min"
        )
        reduce_lr = cb.ReduceLROnPlateau(
            monitor="val_loss", factor=0.2, patience=3, min_lr=0.00001, verbose=1
        )
        epoch_history = EpochHistory()

        return [early_stopping, reduce_lr, epoch_history]

    def start_training(
        self, input_size: int, output_size: int, train_ds: list, validation_ds: list
    ) -> None:
        """Starts training the model using the provided datasets."""
        callbacks = self._create_callbacks()

        self.model = self._build_model(input_size, output_size)
        self.model.fit(
            train_ds,
            validation_data=validation_ds,
            epochs=TFModel.EPOCHS.value,
            verbose=1,
            callbacks=callbacks,
        )

        model_path = dm.model_dir / f"{self.ai_model_name}.h5"
        self.model.save(model_path)

    def start_evaluating(
        self, image_file_list: np.ndarray, true_label_list: np.ndarray
    ) -> tuple[dict[str, int], np.ndarray]:
        """Evaluates the model using a list of images."""
        if image_file_list.size == 0:
            raise ValueError("No images provided for evaluation.")

        model = self._load_model() if self.model is None else self.model
        prediction_result = model.predict(image_file_list, batch_size=256, verbose=0)
        # For binary classification, use thresholding. For multi-class, use argmax
        predictions = np.argmax(prediction_result, axis=1)

        cm = confusion_matrix(true_label_list, predictions, labels=[0, 1])
        TP = np.diag(cm)
        FN = cm.sum(axis=1) - np.diag(cm)
        FP = cm.sum(axis=0) - np.diag(cm)
        TN = cm.sum() - (FP + FN + TP)

        cm_results = {
            "true_pos": int(TP[1]),
            "false_neg": int(FN[1]),
            "false_pos": int(FP[1]),
            "true_neg": int(TN[1]),
        }

        return cm_results, true_label_list != predictions
