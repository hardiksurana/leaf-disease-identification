import numpy as np
import pickle
from scipy.misc import imread, imresize
import sys 
from keras import backend as K

class_names = {
    0: 'late blight', 
    1: 'healthy',
    2: 'septorial leaf spot', 
    3: 'mosaic virus', 
    4: 'bacterial spot', 
    5: 'yellow curved'
}

def predict_disease(file_path):
    K.clear_session()
    model = pickle.load(open("../model/data/model_info/alexnet_trained_model.pkl","rb"), encoding='utf-8')
    train_images = np.load('../model/data/model_info/train_images_alexnet.npy')
    train_images = np.array(train_images)
    mean = np.mean(train_images,axis=(0,1,2,3))
    std = np.std(train_images,axis=(0,1,2,3))
    img = imresize(imread(file_path, mode='RGB'),(227, 227)).astype(np.float32)
    img = (img-mean)/(std+1e-7)
    img = np.expand_dims(img, axis=0)
    out = model.predict(img)
    return class_names[np.argmax(out)]

predict_disease(sys.argv[1])