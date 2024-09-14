from statistics import mode
from tensorflow import keras
import numpy as np
import os

def load_data():
    # load data and split it in test and train set
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    #scale imgs to [0,1] range
    x_train = x_train.astype("float32") / 255
    x_test = x_test.astype("float32") / 255

    #make sure imgs have shape (28, 28, 1)
    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)
    print("x_train shape:", x_train.shape)
    print("y_train shape:", y_train.shape)
    print(x_train.shape[0], "train samples")
    print(x_test.shape[0], "test samples")
    return(x_train, x_test, y_train, y_test)

def make_model(x_train, x_test, y_train, y_test):
    # model parameters
    num_classes = 10
    input_shape = (28, 28, 1)

    model = keras.Sequential(
        [
            keras.layers.Input(shape=input_shape),
            keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            keras.layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
            keras.layers.MaxPooling2D(pool_size=(2, 2)),
            keras.layers.Conv2D(128, kernel_size=(3, 3), activation="relu"),
            keras.layers.Conv2D(128, kernel_size=(3, 3), activation="relu"),
            keras.layers.GlobalAveragePooling2D(),
            keras.layers.Dropout(0.5),
            keras.layers.Dense(num_classes, activation="softmax"),
        ]
    )

    model.summary()
    model.compile(
        loss=keras.losses.SparseCategoricalCrossentropy(),
        optimizer=keras.optimizers.Adam(learning_rate=1e-3),
        metrics=[
            keras.metrics.SparseCategoricalAccuracy(name="acc"),
        ],
    )

    batch_size = 128
    epochs = 20

    callbacks = [
        keras.callbacks.ModelCheckpoint(filepath="model_at_epoch_{epoch}.keras"),
        keras.callbacks.EarlyStopping(monitor="val_loss", patience=2),
    ]

    model.fit(
        x_train,
        y_train,
        batch_size=batch_size,
        epochs=epochs,
        validation_split=0.15,
        callbacks=callbacks,
    )
    score = model.evaluate(x_test, y_test, verbose=0)

### MNIST convnet


x_train, x_test, y_train, y_test = load_data()
#make_model(x_train, x_test, y_train, y_test)

model = keras.saving.load_model('model_at_epoch_10.keras')
score = model.evaluate(x_test, y_test, verbose=0)
#predictions = model.predict(x_test)
print(score)


