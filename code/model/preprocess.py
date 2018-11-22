import os
import numpy as np
from scipy.misc import imread, imresize

count = -2
train_labels = []
train_images = []

for root, dirs, files in os.walk("./dataset/"):
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))        
    count = count + 1
    for file in files:
        print(os.path.join(root, file))
        img = imresize(imread(os.path.join(root, file), mode='RGB'), (227, 227)).astype(np.float32)
        train_images.append(img)
        train_labels.append(count)
        print(len(path) * '---', file)

print(len(train_images))
print(len(train_labels))

#print(train_labels)

np.save('./data/model_info/train_images_alexnet.npy',np.array(train_images))
np.save('./data/model_info/train_labels_alexnet.npy',np.array(train_labels))

# np.save('./data/model_info/train_images_lenet.npy',np.array(train_images))
# np.save('./data/model_info/train_labels_lenet.npy',np.array(train_labels))
