import keras
from keras.layers import Conv2D,Input,Dense,MaxPooling2D,BatchNormalization,ZeroPadding2D,Flatten,Dropout
from keras.models import Model
import numpy as np
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ReduceLROnPlateau, CSVLogger,EarlyStopping,ModelCheckpoint
import pickle
# import matplotlib.pyplot as plt
from scipy.misc import imread, imresize
from numpy.random import permutation

def alexnet():
    
    input_1 = Input(shape=(227,227,3))
    
    conv_1 = Conv2D(96, 11, strides=(4, 4), padding='valid',activation='relu',name='conv_1')(input_1)
    pool_1 = MaxPooling2D((3, 3), strides=(2, 2),name='pool_1')(conv_1)
    norm_1 = BatchNormalization()(pool_1)
    padding_1 = ZeroPadding2D((2,2))(norm_1)
    
    conv_2 = Conv2D(256, 5,padding='valid',activation='relu',name='conv_2')(padding_1)
    pool_2 = MaxPooling2D((3, 3), strides=(2, 2),name='pool_2')(conv_2)
    norm_2 = BatchNormalization()(pool_2)
    padding_2 = ZeroPadding2D((1,1))(norm_2)
    
    conv_3 = Conv2D(384, 3,padding='valid',activation='relu',name='conv_3')(padding_2)
    padding_3 = ZeroPadding2D((1,1))(conv_3)
    conv_4 = Conv2D(384, 3,padding='valid',activation='relu',name='conv_4')(padding_3)
    padding_4 = ZeroPadding2D((1,1))(conv_4)
    conv_5 = Conv2D(256, 3,padding='valid',activation='relu',name='conv_5')(padding_4)
    pool_3 = MaxPooling2D((3, 3), strides=(3, 3),name='pool_3')(conv_5)
    
    dense_1 = Flatten(name="flatten")(pool_3)
    dense_1 = Dense(4096, activation='relu',name='dense_1')(dense_1)
    dense_2 = Dropout(0.5)(dense_1)
    dense_2 = Dense(4096, activation='relu',name='dense_2')(dense_2)
    dense_3 = Dropout(0.5)(dense_2)
    dense_3 = Dense(10,name='dense_3_new')(dense_3)

    model = Model(inputs = input_1,outputs = dense_3)
    return model

model = alexnet()
model.summary()

train_images = np.load('./data/model_info/train_images_lenet.npy')
train_labels = np.load('./data/model_info/train_labels_lenet.npy')

# Test pretrained model
train_images = np.array(train_images)
train_labels = np.array(train_labels)
mean = np.mean(train_images,axis=(0,1,2,3))
std = np.std(train_images,axis=(0,1,2,3))
train_images = (train_images-mean)/(std+1e-7)
num_classes = 10
train_labels = np_utils.to_categorical(train_labels,num_classes)

perm = permutation(len(train_images))
train_images = train_images[perm]
train_labels = train_labels[perm]
val_images = train_images[1:1000]
val_labels = train_labels[1:1000]
new_train= train_images[1000:]
new_labels = train_labels[1000:]

lr_reducer = ReduceLROnPlateau(factor = np.sqrt(0.1), cooldown=0, patience=2, min_lr=0.5e-6)
csv_logger = CSVLogger('./data/model_info/Alexnet.csv')
early_stopper = EarlyStopping(min_delta=0.001,patience=30)
model_checkpoint = ModelCheckpoint('./data/model_info/Alexnet.hdf5',monitor = 'val_loss', verbose = 1,save_best_only=True)


model.compile(loss='categorical_crossentropy',
        optimizer="Adam",
        metrics=['accuracy'])

datagen = ImageDataGenerator(
        featurewise_center=True,  # set input mean to 0 over the dataset
        samplewise_center=True,  # set each sample mean to 0
        featurewise_std_normalization=False,  # divide inputs by std of the dataset
        samplewise_std_normalization=False,  # divide each input by its std
        zca_whitening=False,  # apply ZCA whitening
        rotation_range=20,  # randomly rotate images in the range (degrees, 0 to 180)
        width_shift_range=0.1,  # randomly shift images horizontally (fraction of total width)
        height_shift_range=0.1,  # randomly shift images vertically (fraction of total height)
        horizontal_flip=True,  # randomly flip images
        vertical_flip=False)  # randomly flip images
    
datagen.fit(train_images)

model.fit_generator(datagen.flow(new_train, new_labels, batch_size=12),
                        steps_per_epoch=train_images.shape[0] // 12,
                        validation_data = (val_images,val_labels),
                        epochs=2,verbose=1,callbacks = [lr_reducer,early_stopper,csv_logger,model_checkpoint])


model.fit(train_images, train_labels,
              batch_size=12,
              epochs=2,
              validation_split=0.3,
              shuffle=True,callbacks=[lr_reducer,csv_logger,early_stopper,model_checkpoint])

# serializing our model to a file called model.pkl
pickle.dump(model, open("./data/model_info/alexnet_trained_model.pkl","wb"))
model.save_weights('./data/model_info/alexnet_weights.h5')