'''
module: models
Functions for building networks of various architecture in Keras
'''

import keras
from keras.models import Sequential, Model
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Input, Reshape
import tensorflow as tf
import keras.backend as K

NUM_CLASSES = 46


def residual_layer(input_tensor, num_filters, filter_size=(3,3)):
    """Builds a residual layer on top of input tensor with Keras's Function API
        
        Args:
            input_tensor: tensor
        
        Returns:
            tensor
    """

    num_channels_input_tensor = K.int_shape(input_tensor)[3]
    channels_equal = num_channels_input_tensor == num_filters

    if channels_equal:
        conv_1 = Conv2D(num_filters, filter_size, padding='same')(input_tensor)
        batch_norm_1 = keras.layers.BatchNormalization(axis=3)(conv_1)
    else:
        input_tensor = Conv2D(num_filters, (1,1), padding='same')(input_tensor)
        conv_1 = Conv2D(num_filters, filter_size, padding='same')(input_tensor)
        batch_norm_1 = keras.layers.BatchNormalization(axis=3)(conv_1)
    relu_1 = keras.layers.Activation('relu')(batch_norm_1)
    conv_2 = Conv2D(num_filters, filter_size, padding='same')(relu_1)
    batch_norm_2 = keras.layers.BatchNormalization(axis=3)(conv_2)
    add_1 = keras.layers.add([batch_norm_2, input_tensor])
    add_1 = keras.layers.Activation('relu')(add_1)
    return add_1

def deep_neural_network():
    '''
    This builds a deep vanilla neural network.
    '''
    model = Sequential()
    model.add(Flatten())
    model.add(Dense(2048, activation='relu'))
    model.add(Dense(1024, activation='relu'))
    model.add(Dropout(0.25))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(NUM_CLASSES, activation=tf.nn.softmax))
    model.add(Dropout(0.25))
    return model


def convolutional_neural_network():
    '''
    This builds a deep vanilla neural network.
    '''
    model = Sequential()
    model.add(Reshape((32, 32, 1), input_shape=(32, 32)))
    model.add(Conv2D(8, kernel_size=(3, 3), activation='relu'))
    model.add(Conv2D(16, kernel_size=(3, 3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(32, activation='relu'))
    model.add(Dense(47, activation='softmax'))
    return model


def badass_network():
    '''
    This builds a deep vanilla neural network.
    '''
    model = Sequential()
    input_x = Input(shape=(32, 32))
    x_reshaped = Reshape((32, 32, 1))(input_x)

    conv_1 = Conv2D(4, (5,5), activation='relu')(x_reshaped)
    pool_1 = MaxPooling2D(pool_size=(2,2))(conv_1)


    res_1 = residual_layer(pool_1, 4, (3,3))
    res_2 = residual_layer(res_1, 4, (3,3))
    res_3 = residual_layer(res_2, 8, (3,3))

    pool_2 = MaxPooling2D(pool_size=(2,2))(res_3)
    model.add(Dropout(0.2))

    flat = Flatten()(pool_2)

    fc_2 = Dense(128, activation='relu')(flat)
    fc_3 = Dense(64, activation='relu')(fc_2)
    model.add(Dropout(0.1))


    output_layer = Dense(NUM_CLASSES, activation=tf.nn.softmax)(fc_3)

    badass_model = Model(inputs=[input_x], outputs=output_layer)

    return badass_model
