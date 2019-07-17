from typing import Tuple
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.layers import Dense
def mlp(input_shape: Tuple[int,...],
        output_shape: Tuple[int,...],
        layer_size: int = 128,
        dropout_amount: float = 0.2,
        num_layers: int = 3) -> Model:
    num_classes = output_shape[0]
    model = Sequential()
    model.add(Flatten(input_shape = input_shape))
    for i in range(num_layers):
        model.add(Dense(layer_size, activation = 'relu'))
        model.add(dropout_amount)
    model.add(Dense(num_classes, activation = 'softmax'))
    return model
