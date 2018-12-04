import os, sys, glob, csv
import pandas as pd
import random

rootDirDataset = 'C:\\Apps\\MESTRADO\\Videos\\'
fileAnnotation = rootDirDataset + 'dataset\\' + 'dataset.csv'

dirTrain = rootDirDataset + 'dataset\\' + 'train'
dirVal = rootDirDataset + 'dataset\\' + 'val'
dirTest = rootDirDataset + 'dataset\\' + 'test'

txTrain = 0.7
txVal = 0.2
txTest = 0.1

for d in [dirTrain, dirVal, dirTest]:
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

newClassNaoPulaCatraca = random.choice([i for i in dataClassNaoPulaCatraca if i not in trainClassNaoPulaCatraca])
print(" ")
