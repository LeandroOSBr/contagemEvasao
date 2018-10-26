#import os
#import csv
import pandas as pd
import cv2
import numpy as np

from keras.optimizers import SGD, RMSprop
from keras.utils import np_utils, generic_utils

import matplotlib
import matplotlib.pyplot as plt
from sklearn.cross_validation import train_test_split
from sklearn import cross_validation
from sklearn import preprocessing


# image specification
img_rows,img_cols,img_depth=112,112,12

# Training data
X_tr=[]           # variable to store entire dataset

#Reading list files in Dataset
dataA = pd.read_csv('./dataset/dataset.csv',sep=';').to_dict(orient="row")

dataClassSimPulaCatraca = []
dataClassNaoPulaCatraca = []

for dataR in dataA:
    if dataR['class'] == 'NaoPulouCatraca':
        dataClassNaoPulaCatraca.append(dataR['file'])
    if dataR['class'] == 'SimPulouCatraca':
        dataClassSimPulaCatraca.append(dataR['file'])

#Reading SimPulaCatraca action class  
for vid in dataClassSimPulaCatraca:
    frames = []
    cap = cv2.VideoCapture(vid)
    fps = cap.get(cv2.CAP_PROP_FPS)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print ("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))

    for k in range(length):
        ret, frame  = cap.read()
        frame = cv2.resize(frame,(img_rows,img_cols))
        frames.append(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cap.release()
    cv2.destroyAllWindows()

    input=np.array(frames)

    print(input.shape)
    ipt=np.rollaxis(np.rollaxis(input,2,0),2,0)
    print(ipt.shape)

    X_tr.append(ipt)

#Reading SimPulaCatraca action class  
for vid in dataClassNaoPulaCatraca:
    frames = []
    cap = cv2.VideoCapture(vid)
    fps = cap.get(cv2.CAP_PROP_FPS)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print ("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))

    for k in range(length):
        ret, frame  = cap.read()
        frame = cv2.resize(frame,(img_rows,img_cols))
        frames.append(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cap.release()
    cv2.destroyAllWindows()

    input=np.array(frames)

    print(input.shape)
    ipt=np.rollaxis(np.rollaxis(input,2,0),2,0)
    print(ipt.shape)

    X_tr.append(ipt)

X_tr_array = np.array(X_tr)   # convert the frames read into array

num_samples = len(X_tr_array) 
print(num_samples)

#TODO:
# No dataset, as imagens estão com dimensão diferentes!
# 1. Resize das imagens ou
# 2. Refaz o DS.

#Assign Label to each class
#TODO

# CNN Training parameters

batch_size = 2
nb_classes = 6
nb_epoch =50

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train, nb_classes)

# number of convolutional filters to use at each layer
nb_filters = [32, 32]

# level of pooling to perform at each layer (POOL x POOL)
nb_pool = [3, 3]

# level of convolution to perform at each layer (CONV x CONV)
nb_conv = [5,5]

# Pre-processing

train_set = train_set.astype('float32')
train_set -= np.mean(train_set)
train_set /=np.max(train_set)

# Define model

model = Sequential()
model.add(Convolution3D(nb_filters[0],nb_depth=nb_conv[0], nb_row=nb_conv[0], nb_col=nb_conv[0], input_shape=(1, img_rows, img_cols, patch_size), activation='relu'))
model.add(MaxPooling3D(pool_size=(nb_pool[0], nb_pool[0], nb_pool[0])))
model.add(Dropout(0.5))
model.add(Flatten())
model.add(Dense(128, init='normal', activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(nb_classes,init='normal'))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy', optimizer='RMSprop')
  
# Split the data
X_train_new, X_val_new, y_train_new,y_val_new =  train_test_split(train_set, Y_train, test_size=0.2, random_state=4)


# Train the model

hist = model.fit(X_train_new, y_train_new, validation_data=(X_val_new,y_val_new),
          batch_size=batch_size,nb_epoch = nb_epoch,show_accuracy=True,shuffle=True)


#hist = model.fit(train_set, Y_train, batch_size=batch_size,
#         nb_epoch=nb_epoch,validation_split=0.2, show_accuracy=True,
#           shuffle=True)


 # Evaluate the model
score = model.evaluate(X_val_new, y_val_new, batch_size=batch_size, show_accuracy=True)
print('Test score:', score[0])
print('Test accuracy:', score[1]) 



# Plot the results
train_loss=hist.history['loss']
val_loss=hist.history['val_loss']
train_acc=hist.history['acc']
val_acc=hist.history['val_acc']
xc=range(100)

plt.figure(1,figsize=(7,5))
plt.plot(xc,train_loss)
plt.plot(xc,val_loss)
plt.xlabel('num of Epochs')
plt.ylabel('loss')
plt.title('train_loss vs val_loss')
plt.grid(True)
plt.legend(['train','val'])
print(plt.style.available) # use bmh, classic,ggplot for big pictures
plt.style.use(['classic'])

plt.figure(2,figsize=(7,5))
plt.plot(xc,train_acc)
plt.plot(xc,val_acc)
plt.xlabel('num of Epochs')
plt.ylabel('accuracy')
plt.title('train_acc vs val_acc')
plt.grid(True)
plt.legend(['train','val'],loc=4)
#print plt.style.available # use bmh, classic,ggplot for big pictures
plt.style.use(['classic'])