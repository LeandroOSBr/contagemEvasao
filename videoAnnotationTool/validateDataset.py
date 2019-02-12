# coding=utf-8
import os, sys, glob, cv2,csv
import pandas as pd

limparArquivosNaoAnotado = True
limparArquivosNao11Quadros = True

rootDirDataset = 'C:\\Apps\\MESTRADO\\Videos\\'
fileAnnotation = rootDirDataset + 'dataset\\' + 'dataset_w_originalfile_position_roi.csv'

# Lista arquivos anotados que são inexistentes:
dataA = pd.read_csv(fileAnnotation,sep=';').to_dict(orient="row")
listFileYesExist = []
listFileNoExist = []
for dataR in dataA:
    fileName = rootDirDataset+dataR['file']
    if os.path.isfile(fileName):
        listFileYesExist.append(fileName)
    else:
        listFileNoExist.append(fileName)

print("Count SIM existe: ", len(listFileYesExist))
print("Count NAO existe: ", len(listFileNoExist))
print("--------------------------------------------")

# Lista FPS e Quantidade de Frames
fpsMenor3 = []
fps3 = []
fps4 = []
fps5 = []
fpsMaior5 = []
l11 = []
lOutros = []

for file in listFileYesExist:
    captura = cv2.VideoCapture(file)
    length = int(captura.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(captura.get(cv2.CAP_PROP_FPS))
    if fps < 3:
        fpsMenor3.append(file)
    elif fps == 3:
        fps3.append(file)
    elif fps == 4:
        fps4.append(file)
    elif fps == 5:
        fps5.append(file)
    elif fps > 5:
        fpsMaior5.append(file)

    if length == 11:
        l11.append(file)
    else:
        lOutros.append(file)

print("FPS < 3: ", len(fpsMenor3))
print("FPS = 3: ", len(fps3))
print("FPS = 4: ", len(fps4))
print("FPS = 5: ", len(fps5))
print("FPS < 5: ", len(fpsMaior5))
print("--------------------------------------------")
print("Quadros  11: ", len(l11))
print("Quadros !11: ", len(lOutros))

if limparArquivosNao11Quadros:
    dataA = pd.read_csv(fileAnnotation,sep=';',encoding='utf-8')
    for index, row in dataA.iterrows():        
        fileName = rootDirDataset+row['file']
        captura = cv2.VideoCapture(fileName)
        length = int(captura.get(cv2.CAP_PROP_FRAME_COUNT))
        if length != 11:
            print("Excluindo registro: ", index, " - ", row['file'])
            dataA.drop(dataA.index[[index]],inplace = True)            
    print(dataA.shape)
    dataA.to_csv(fileAnnotation, sep=';',index=False, encoding='utf8')

# Arquivos de video no diretório que não está anotado
fileListRootDirDataset = glob.glob(rootDirDataset + 'dataset\\*.avi')
print("--------------------------------------------")
print("Quantidade de Arquivos: ", len(fileListRootDirDataset))
fileSimAnotado = []
fileNaoAnotado = []
for fileDir in fileListRootDirDataset:
    #Existe na Anotação?
    if fileDir in listFileYesExist:
        fileSimAnotado.append(fileDir)
    else:
        fileNaoAnotado.append(fileDir)

print("Arquivos SIM Anotados: ", len(fileSimAnotado))
print("Arquivos NAO Anotados: ", len(fileNaoAnotado))

arquivoSimExcluido = []
arquivoNaoExcluido = []

if limparArquivosNaoAnotado:
    # Remover do diretório os arquivos que não estão anotados
    for file in fileNaoAnotado:
        r = os.remove(file)
        if os.path.isfile(file):
            # print("Erro ao excluir arquivo: ", file)
            arquivoNaoExcluido.append(file)
        else:
            # print("Arquivo '", file, "' excluido com sucesso!")
            arquivoSimExcluido.append(file)

    print("Arquivos SIM excluidos: ", len(arquivoSimExcluido))
    print("Arquivos NAO excluidos: ", len(arquivoNaoExcluido))