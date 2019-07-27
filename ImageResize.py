from PIL import Image, ImageFilter
import numpy as np

def resizeImage(img):
    im = Image.open(img)
    resize_image = im.resize((32, 32), Image.ANTIALIAS)
    image_arr = np.asarray(resize_image)
    return image_arr[:,:,0]