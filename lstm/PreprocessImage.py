import numpy as np
import cv2
from keras.preprocessing import image

def process(img):
    img = np.array(img)
    (wt, ht) = (128, 32)
    (h, w) = img.shape
    fx = w / wt
    fy = h / ht
    f = max(fx, fy)
    newSize = (max(min(wt, int(w / f)), 1), max(min(ht, int(h / f)), 1)) # scale according to f (result at least 1 and at most wt or ht)
    img = cv2.resize(np.array(img), newSize)
    target = np.ones([ht, wt]) * 255
    target[0:newSize[1], 0:newSize[0]] = img
    img = cv2.transpose(target)

    (m, s) = cv2.meanStdDev(img)
    m = m[0][0]
    s = s[0][0]
    img = img - m
    img = img / s if s>0 else img

    img = np.expand_dims(img, axis=2)
    return img