#import os
#import csv
import pandas as pd
import cv2
import numpy as np


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