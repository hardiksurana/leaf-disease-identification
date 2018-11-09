import numpy as np
import pickle
from scipy.misc import imread, imresize

class_names = {
    0: 'curl_virus', 
    1: 'late_blight', 
    2: 'early_blight', 
    3: 'spider_mites', 
    4: 'healthy',
    5: 'septorial_leaf_spot', 
    6: 'target_spot', 
    7: 'mosaic_virus', 
    8: 'bacterial_spot', 
    9: 'leaf_mold'
}

def predict_disease(file_path):
    model = pickle.load(open("./model/data/model_info/alexnet_trained_model.pkl","rb"), encoding='utf-8')
    train_images = np.load('./model/data/model_info/train_images_lenet.npy')
    train_images = np.array(train_images)
    mean = np.mean(train_images,axis=(0,1,2,3))
    std = np.std(train_images,axis=(0,1,2,3))
    img = imresize(imread(file_path, mode='RGB'),(227, 227)).astype(np.float32)
    img = (img-mean)/(std+1e-7)
    img = np.expand_dims(img, axis=0)
    # out = model._make_predict_function()
    out = model.predict(img) 
    return class_names[np.argmax(out)]
