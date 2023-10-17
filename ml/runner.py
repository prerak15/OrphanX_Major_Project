import tensorflow

from tensorflow.keras.models import load_model

import numpy as np
import cv2
from keras_vggface.utils import preprocess_input

def process(img1, img2, img3):
    model = load_model('ml/input/vgg_face.h5')
    #model.summary()
    test_path_p = "parent/"
    test_path_c = "static/"
    def read_img(path):
        img = cv2.imread(path)
        img = np.array(img).astype(np.float64)
        return preprocess_input(img, version=2)

    X1 = test_path_p + img1
    X1 = np.array([read_img(X1)])

    X2 = test_path_p + img2
    X2 = np.array([read_img(X2)])
    
    X3 = test_path_c + img3
    X3 = np.array([read_img(X3)])

    pred = model.predict([X1, X2, X3])
    return pred
    """
face00443 child chinese
face00426 parent chinese
face00438 parent black
"""

