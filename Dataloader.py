import numpy as np

def load_data():
    dataset = np.load('dataset/dataset.npz')
    train_label = dataset['arr_1']
    train_image = dataset['arr_0']
    test_label = dataset['arr_3']
    test_image = dataset['arr_2']
    return (train_image, train_label), (test_image, test_label)