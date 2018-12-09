import pandas as pd
import cv2
import numpy as np

import keras

from keras.optimizers import SGD, RMSprop
from keras.utils import np_utils, generic_utils
from keras.models import Sequential, load_model

from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.layers.convolutional import Convolution3D, MaxPooling3D

import matplotlib
import matplotlib.pyplot as plt

import keras.callbacks as kcall

import glob, os

projectDir = 'C:\\Apps\\MESTRADO\\'
dirDataset = projectDir + 'datasetFolder\\'

train_dir = dirDataset + 'train'
val_dir = dirDataset + 'val'
test_dir = dirDataset + 'test'

# image specification
img_rows,img_cols,img_depth=112,112,11

# Percentual de Itens de carga do Dataset. Utilizado para economizar uso de recurso durante os primeiros treinos.
txUsoDataset = 0.5

def get_data(folder):
    frames = []
    X = []
    y = []
    for folderName in os.listdir(folder):
        if not folderName.startswith('.'):
            if folderName in ['NaoPulaCatraca']:
                label = 0
            elif folderName in ['SimPulaCatraca']:
                label = 1
            else:
                label = 2
            for image_filename in (os.listdir(folder + '\\' + folderName)):
                fileName = folder + '\\' + folderName + '\\' + image_filename
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
                    #printm()
                    print("X: ",len(X))
                    print("y: ",len(y))
    X = np.asarray(X)
    y = np.asarray(y)
    return X,y

X_train, y_train = get_data(train_dir)