import os, sys, glob, csv, shutil
import pandas as pd
import random

rootDirDataset = 'C:\\Apps\\MESTRADO\\Videos\\'
fileAnnotation = rootDirDataset + 'dataset\\' + 'dataset_w_originalfile_position_roi.csv'

dirTrain = rootDirDataset + 'dataset\\' + 'train'
dirVal = rootDirDataset + 'dataset\\' + 'val'
dirTest = rootDirDataset + 'dataset\\' + 'test_real'

txTrain = 0.0
txVal = 0.0
txTest = 1.0

for d in [dirTrain, dirTrain+'\\SimPulaCatraca', dirTrain+'\\NaoPulaCatraca', dirVal, dirVal+'\\SimPulaCatraca', dirVal+'\\NaoPulaCatraca', dirTest,dirTest+'\\SimPulaCatraca', dirTest+'\\NaoPulaCatraca']:
    try:
        os.mkdir(d)        
    except OSError as e:
        print(e.strerror, ": ", e.filename)

dataA = pd.read_csv(fileAnnotation,sep=';').to_dict(orient="row")
dataClassSimPulaCatraca = []
dataClassNaoPulaCatraca = []
for dataR in dataA:
    if dataR['class'] == 'NaoPulouCatraca':
        dataClassNaoPulaCatraca.append(dataR['file'])
    if dataR['class'] == 'SimPulouCatraca':
        dataClassSimPulaCatraca.append(dataR['file'])
print("Anotacao - NAO Pulou Catraca", len(dataClassNaoPulaCatraca))
print("Anotacao - SIM Pulou Catraca", len(dataClassSimPulaCatraca))

trainClassNaoPulaCatraca = random.sample(dataClassNaoPulaCatraca, int(txTrain * len(dataClassNaoPulaCatraca)))
trainClassSimPulaCatraca = random.sample(dataClassSimPulaCatraca, int(txTrain * len(dataClassSimPulaCatraca)))

newDataAClassSimPulaCatraca = [x for x in dataClassSimPulaCatraca if x not in trainClassSimPulaCatraca]
newDataAClassNaoPulaCatraca = [x for x in dataClassNaoPulaCatraca if x not in trainClassNaoPulaCatraca]

valClassSimPulaCatraca = random.sample(newDataAClassSimPulaCatraca, int(txVal * len(dataClassSimPulaCatraca)))
valClassNaoPulaCatraca = random.sample(newDataAClassNaoPulaCatraca, int(txVal * len(dataClassNaoPulaCatraca)))

testClassSimPulaCatraca = [x for x in newDataAClassSimPulaCatraca if x not in valClassSimPulaCatraca]
testClassNaoPulaCatraca = [x for x in newDataAClassNaoPulaCatraca if x not in valClassNaoPulaCatraca]

print("LEN Train - Sim Pula Catraca: ", len(trainClassSimPulaCatraca))
print("LEN Train - Nao Pula Catraca: ", len(trainClassNaoPulaCatraca))

print("LEN Val - Sim Pula Catraca: ", len(valClassSimPulaCatraca))
print("LEN Val - Nao Pula Catraca: ", len(valClassNaoPulaCatraca))

print("LEN Test - Sim Pula Catraca: ", len(testClassSimPulaCatraca))
print("LEN Test - Nao Pula Catraca: ", len(testClassNaoPulaCatraca))

for f in trainClassSimPulaCatraca:
    shutil.copy(rootDirDataset+f,dirTrain+'\\SimPulaCatraca\\')
for f in trainClassNaoPulaCatraca:
    shutil.copy(rootDirDataset+f,dirTrain+'\\NaoPulaCatraca\\')

for f in valClassSimPulaCatraca:
    shutil.copy(rootDirDataset+f,dirVal+'\\SimPulaCatraca\\')
for f in valClassNaoPulaCatraca:
    shutil.copy(rootDirDataset+f,dirVal+'\\NaoPulaCatraca\\')

for f in testClassSimPulaCatraca:
    shutil.copy(rootDirDataset+f,dirTest+'\\SimPulaCatraca\\')
for f in testClassNaoPulaCatraca:
    shutil.copy(rootDirDataset+f,dirTest+'\\NaoPulaCatraca\\')