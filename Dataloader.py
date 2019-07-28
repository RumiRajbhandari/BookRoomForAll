import numpy as np

def load_data():
    dataset = np.load('dataset/dataset.npz')
    my_dict = {1: 'क', 2: 'ख', 3: 'ग', 4: 'घ', 5: 'ङ', 6:'च', 7: 'छ', 8:'ज',9:'झ',10:'ञ',11:'ट',12:'ठ',13:'ड',14:'ढ',15:'ण', 16:'त',17:'थ',18:'द', 19:'ध',20:'न',21:'प',22:'फ',23:'ब',24:'भ',25:'म', 26:'य', 27:'र', 28:'ल', 29:'व', 30:'श', 31:'ष', 32:'स', 33:'ह', 34:'क्ष', 35:'त्र', 36:'ज्ञ', 37:'0', 38:'1', 39:'2', 40:'3', 41:'4', 42:'5', 43:'6', 44:'7', 45:'8', 46:'9' }

    train_label = dataset['arr_1']
    train_image = dataset['arr_0']
    test_label = dataset['arr_3']
    test_image = dataset['arr_2']
    return (train_image, train_label), (test_image, test_label), my_dict