import os
import json
from datetime import datetime
from re import S
import tensorflow as tf
from tensorflow.keras import layers as Layers, models as Models, optimizers as Optimizer, callbacks as cb
from tensorflow.keras.models import load_model
from tensorflow.keras.callbacks import ModelCheckpoint

from apis.utils.directory import dire
from apis.CMT.training.dataset import create_image_dataset
from apis.CMT.training.Epoch_update import send_epoch_updates
from core.config import Settings


class TrainingCallback(cb.Callback):
    def __init__(self, websocket):
        self.websocket = websocket

    async def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        # Include more metrics as needed for plotting
        data = {
            'epoch': epoch,
            'accuracy': logs.get('accuracy'),
            'loss': logs.get('loss'),
            'val_accuracy': logs.get('val_accuracy'),
            'val_loss': logs.get('val_loss')
        }
        await self.websocket.send_text(json.dumps(data))


async def train_model(selected_dir, epochs, early_stopping=False, best_model=False, reduce_lr_on_plateau=False, websocket=None, checkpoint=False):
    inputShape = Settings.INPUTSHAPE
    seed = Settings.SEED
    ker = Settings.KER
    sker = Settings.SKER
   
    # Use create_image_dataset to get training and validation datasets
    (train_ds, train_info), (validation_ds, validation_info) = create_image_dataset(selected_dir)

    model_main = dire.models_path
    checkpoint_main = os.path.join(model_main, "checkpoint")
    os.makedirs(checkpoint_main, exist_ok=True)
    checkpoint_path = os.path.join(checkpoint_main, "checkpoint_{epoch:02d}.h5")
    best_model_path = os.path.join(model_main, "best_model.h5")
    latest_checkpoint = best_model_path if os.path.exists(best_model_path) else None

    # Name of the model can be save as the chip type and datetime
    model_save = os.path.join(model_main, datetime.now().strftime("%Y%m%d_%H%M%S_") + "model.h5")

    log_dir="logs/fit/" + datetime.now().strftime("%Y%m%d-%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
    validation_ds = validation_ds.cache().prefetch(buffer_size=AUTOTUNE)

    # Check if there is a checkpoint
    if checkpoint and latest_checkpoint:
        print("Resuming from checkpoint.")
        model = load_model(latest_checkpoint)
    else:
        # Define the model
        model = Models.Sequential([
            Layers.Rescaling(1./255, input_shape=inputShape),
            Layers.RandomFlip("horizontal_and_vertical", seed=seed),
            Layers.Conv2D(16, kernel_size=ker, activation='relu', padding='same'),
            Layers.Conv2D(32, kernel_size=sker, activation='relu', padding='same'),
            Layers.MaxPool2D(2, 2),
            Layers.Conv2D(64, kernel_size=ker, activation='relu', padding='same'),
            Layers.Conv2D(128, kernel_size=sker, activation='relu', padding='same'),
            Layers.MaxPool2D(3, 2),
            Layers.Conv2D(256, kernel_size=ker, activation='relu', padding='same'),
            Layers.Conv2D(512, kernel_size=sker, activation='relu', padding='same'),
            Layers.AveragePooling2D(3),
            Layers.Flatten(),
            Layers.Dropout(0.3),
            Layers.Dense(len(train_info['classes']), activation='softmax')  # Match number of classes
        ])

    model.compile(optimizer=Optimizer.Adam(learning_rate=0.001), loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    # Callbacks
    log_dir = "logs/fit/" + datetime.now().strftime("%Y%m%d_%H%M%S")
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
    callbacks = [tensorboard_callback]

    callbacks_dict = {
        cb.EarlyStopping(monitor='val_loss', patience=7, verbose=1, mode='min'): epochs > 50 and early_stopping,
        cb.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.00001, verbose=1): epochs > 50 and reduce_lr_on_plateau,
        ModelCheckpoint(best_model_path, monitor='val_loss', save_best_only=True, verbose=1): best_model,
        ModelCheckpoint(checkpoint_path, save_weights_only=False, monitor='val_accuracy', mode='max', save_best_only=False, save_freq='epoch'): checkpoint,
        TrainingCallback(websocket): websocket is not None
    }

        
    if websocket is not None:
        callbacks.append(TrainingCallback(websocket))


    for callback, condition in callbacks_dict.items():
        if condition:
            callbacks.append(callback)

  
    history = model.fit(
        train_ds,
        validation_data=validation_ds,
        epochs=epochs,
        callbacks=callbacks
    )


    model.save(model_save)
    print(f"Model saved at {model_save}")

    epoch_metrics = []
    for epoch in range(len(history.history['accuracy'])):
        epoch_data = {
            'epoch': epoch + 1,
            'training_accuracy': history.history['accuracy'][epoch],
            'training_loss': history.history['loss'][epoch],
            'validation_accuracy': history.history['val_accuracy'][epoch],
            'validation_loss': history.history['val_loss'][epoch]
        }
        epoch_metrics.append(epoch_data)

    if websocket:
        await send_epoch_updates(websocket, epoch_metrics)


    # Delete all checkpoints except the last one based on the time modified
    checkpoint_files = [f for f in os.listdir(checkpoint_main) if f.startswith("checkpoint")]
    # Sort files by modification time
    checkpoint_files.sort(key=lambda x: os.path.getmtime(os.path.join(checkpoint_main, x)))
    # Keep the most recently modified file, delete the rest
    for file in checkpoint_files[:-1]:
        os.remove(os.path.join(checkpoint_main, file))
        
    return epoch_metrics




