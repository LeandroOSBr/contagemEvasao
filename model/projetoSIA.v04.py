# -*- coding: utf-8 -*-
"""projetoSIA.v04.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sxaHdFj65v0Uuu9_9rwjm2qhvEXsSIZW

## Derivado do projetoSIA.v01
### -> ESte foi criado para utilizar diretórios separados de Train, Val e Test.

### Google Drive Mount
"""

"""### Start Project"""

import pandas as pd
import cv2
import numpy as np

import keras

from keras.optimizers import SGD, RMSprop
from keras.utils import np_utils, generic_utils
from keras.models import Sequential, load_model


from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution3D, MaxPooling3D
from keras.layers.normalization import BatchNormalization

import matplotlib
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import model_selection
from sklearn import preprocessing

import keras.callbacks as kcall

import glob, os
from tqdm import tqdm

# image specification
img_rows,img_cols,img_depth=112,112,11

# Training data
X_tr=[]           # variable to store entire dataset

nb_classes = 2
num_classes = 2

projectDir = 'C:\\Apps\\MESTRADO\\'
dirDataset = projectDir + 'datasetFolder\\'

train_dir = dirDataset + 'train'
val_dir = dirDataset + 'val'
test_dir = dirDataset + 'test'

# Função para fazer o Load do Dataset
def load_data(folder):
  frames = []
  X = []
  y = []
  for folderName in tqdm(os.listdir(folder)):
    if not folderName.startswith('.'):
      if folderName in ['NaoPulaCatraca']:
        label = 0
      elif folderName in ['SimPulaCatraca']:
        label = 1
      else:
        label = 2
      for image_filename in (os.listdir(folder + '/' + folderName)):
        fileName = folder + '/' + folderName + '/' + image_filename
        if fileName is not None:
          cap = cv2.VideoCapture(fileName)
          fps = cap.get(cv2.CAP_PROP_FPS)
          length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))                    
          for k in range(length):
              ret, frame  = cap.read()
              frame = cv2.resize(frame,(img_rows,img_cols))
              frames.append(frame)
          if cv2.waitKey(1) & 0xFF == ord('q'):
              break
          cap.release()
          cv2.destroyAllWindows()
          input=np.array(frames)
          ipt=np.rollaxis(np.rollaxis(input,2,0),2,0)
          X.append(ipt)
          y.append(label)
          frames = []
  #X = np.asarray(X)
  #y = np.asarray(y)
  return X,y

X_train, y_train = load_data(train_dir)
X_train_array = np.array(X_train)

X_val, y_val = load_data(val_dir)
X_val_array = np.array(X_val)

X_test, y_test = load_data(test_dir)
X_test_array = np.array(X_test)

"""# Imprime tamanho Dataset"""

def count_labels(y):
  y_label_0 = []
  y_label_1 = []
  for y_label in y:
    if y_label == 0:
      y_label_0.append(y_label)
    if y_label == 1:
      y_label_1.append(y_label)
  return len(y_label_0), len(y_label_1)

y_train_0, y_train_1 = count_labels(y_train)
y_val_0, y_val_1 = count_labels(y_val)
y_test_0, y_test_1 = count_labels(y_test)

Datasets = ['Train', 'Val', 'Test']
label_0 = [y_train_0, y_val_0, y_test_0]
label_1 = [y_train_1, y_val_1, y_test_1]
positions = [0, 1, 2]
positions2 = [0.3, 1.3, 2.3]
positions3 = [0.15, 1.15, 2.15]
classes = ['Nao Pula Catraca','Sim Pula Catraca']

plt.bar(positions, label_0, width=0.3, color='blue')
plt.bar(positions2, label_1, width=0.3, color='red')

plt.title("Amostas em cada Dataset")
plt.xticks(positions3, Datasets)
plt.xlabel("Datasets")
plt.ylabel("Quantidades")
plt.legend(classes,loc=0)

plt.show()

"""# Rede"""

train_data = X_train_array, y_train
val_data = X_val_array, y_val
test_data = X_test_array, y_test

X_train, y_train = (train_data[0],train_data[1])
X_val, y_val = (val_data[0],val_data[1])
X_test, y_test = (test_data[0],test_data[1])

train_set = X_train
val_set = X_val
test_set = X_test

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train)
Y_val = np_utils.to_categorical(y_val)
Y_test = np_utils.to_categorical(y_test)

# Pre-processing

train_set = train_set.astype('float32')
train_set -= np.mean(train_set)
train_set /=np.max(train_set)

val_set = val_set.astype('float32')
val_set -= np.mean(val_set)
val_set /=np.max(val_set)

test_set = test_set.astype('float32')
test_set -= np.mean(test_set)
test_set /=np.max(test_set)

patch_size = img_depth

# CNN Training parameters

batch_size = 20
nb_epoch =40

# convert class vectors to binary class matrices
Y_train = np_utils.to_categorical(y_train)

kernel_size = [img_rows,img_cols,img_depth]

"""# Início da criação do Modelo"""

# Define model

model = Sequential()

model.add(Convolution3D(
  filters=512,
  kernel_size=11,
  input_shape=(112,112,11,3),
  activation='sigmoid',
  strides=2,
  name='conv1'
  ))

model.add(BatchNormalization())

model.add(MaxPooling3D(pool_size=(3,3,1)))

model.add(Convolution3D(
  filters=256,
  kernel_size=1,
  activation='relu',
  strides=1,
  name='conv2'
  ))

model.add(MaxPooling3D(pool_size=(2, 2, 1)))

model.add(Convolution3D(
  filters=256,
  kernel_size=1,
  activation='relu',
  strides=1,
  name='conv3'
  ))

model.add(Convolution3D(
  filters=128,
  kernel_size=1,
  activation='relu',
  strides=1,
  name='conv4'
  ))

model.add(Convolution3D(
  filters=128,
  kernel_size=1,
  activation='relu',
  strides=1,
  name='conv5'
  ))

model.add(MaxPooling3D(pool_size=(2, 2, 1),name='MAX_3D'))

model.add(Dense(256, kernel_initializer='normal', activation='relu'))

model.add(Dropout(0.5))

model.add(Dense(128, kernel_initializer='normal', activation='relu'))

#model.add(Dropout(0.5))

model.add(Flatten())

model.add(Dense(1,kernel_initializer='normal',activation='softmax'))
#model.add(Activation('softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)

rmsp = RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=1e-6)

#model.compile(loss='binary_crossentropy', optimizer='RMSprop',metrics=['accuracy'])
#model.compile(loss='binary_crossentropy', optimizer=sgd,metrics=['accuracy'])
model.compile(loss='binary_crossentropy', optimizer=rmsp,metrics=['accuracy'])

early_stop = kcall.EarlyStopping(monitor = 'acc', min_delta=0.0001)

class LossHistory(kcall.Callback):
    def on_train_begin(self, logs={}):
        self.losses = []
        self.acc = []

    def on_batch_end(self, batch, logs={}):
        self.losses.append(logs.get('loss'))
        self.acc.append(logs.get('acc'))

history = LossHistory()

#model.summary()

df = pd.DataFrame(columns=["Name", "Input", "output", "Input Shape", "Output Shape"])
i = 0
for layer in model.layers:
  df.loc[i] = [layer.name , layer.input, layer.output, layer.input_shape, layer.output_shape]
  i += 1
  
df.style

# Train the model

hist = model.fit(train_set, y_train, validation_data=(val_set,y_val),
          batch_size=batch_size,epochs = nb_epoch,
          #shuffle=True, 
          callbacks=[history])

score = model.evaluate(X_test, y_test, batch_size=batch_size)
print('Test score:', score[0])
print('Test accuracy:', score[1])

# Plot the results
train_loss=hist.history['loss']
val_loss=hist.history['val_loss']
train_acc=hist.history['acc']
val_acc=hist.history['val_acc']
xc=range(nb_epoch)

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

