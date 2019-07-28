from PIL import Image, ImageFilter,ImageOps
import numpy as np
import tensorflow as tf

from keras.preprocessing import image

def resizeImage(img):
    test_image = image.load_img(img, target_size = (32,32), color_mode="grayscale")
    test_image = ImageOps.invert(test_image)
    test_image = tf.keras.utils.normalize(test_image, axis=1)
    test_image = image.img_to_array(test_image)
    test_image = test_image.reshape((test_image.shape[0], -1), order='F')
    test_image = np.expand_dims(test_image, axis = 0)
    return test_image