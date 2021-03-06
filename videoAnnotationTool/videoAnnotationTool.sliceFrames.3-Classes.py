# USE:
#   [ESC]: Exit
#   [SPACE BAR]: Pause
#   [NumPad #4]: Back any frames
#   [NumPad #6]: Forward any frames
#   [NumPad -]: Down FPS
#   [Num Pad +]: Up FPS
#   [r]: Start video record
#   [n]: Next video
#   [p]: Previus video

import time
# Para facilitar escolha do item a ser anotado!
#import tkinter as tk
#import tkinter.ttk as ttk
import easygui
import os, sys, glob
import pandas as pd

import cv2

def endFileRecord():
    global record
    global startRecord
    global fps
    global out
    global originalFps
    global dataClassNaoPulaCatraca
    global dataClassSimPulaCatraca
    global dataClassSimPassouPorBaixo
    global fileList
    global numFileList
    global pt1
    global pt2
    global actualFrame
    record = False    
    startRecord = False
    out.release()
    #print("Out released")
    fps = originalFps
    a = open(fileAnnotation,"a+")

    response = easygui.enterbox("Insira a Classe: s (Sim, Pulou catraca), n (Não pulou catraca) ou b (Sim, Passou por Baixo?")

    # response = input("Por favor, informe a classe: ")
    if response == 's':
        txtFile = '\nSimPulouCatraca' + ';' + fr + ';' + str(actualFrame) + ';' + str(fileList[numFileList]) + ';' + str(pt1) + ';' + str(pt2)
        a.write(txtFile)
        a.close
    elif response == 'n':
        txtFile = '\nNaoPulouCatraca' + ';' + fr + ';' + str(actualFrame) + ';' + str(fileList[numFileList]) + ';' + str(pt1) + ';' + str(pt2)
        a.write(txtFile)
        a.close
    elif response == 'b':
        txtFile = '\nSimPassouPorBaixo' + ';' + fr + ';' + str(actualFrame) + ';' + str(fileList[numFileList]) + ';' + str(pt1) + ';' + str(pt2)
        a.write(txtFile)
        a.close
    
    print("Anotacao - NAO Pulou Catraca", len(dataClassNaoPulaCatraca))
    print("Anotacao - SIM Pulou Catraca", len(dataClassSimPulaCatraca))
    print("Anotacao - SIM Passou por Baixo", len(dataClassSimPassouPorBaixo))
    print("-------------------------------------")
    print("TOTAL: ",len(dataClassNaoPulaCatraca) + len(dataClassSimPulaCatraca) + len(dataClassSimPassouPorBaixo))

def startFileRecord():
    global startRecord
    global fr
    global recordFile
    global fps
    global out
    global originalFps
    global cropped
    global roiZoom
    global thicknessLine
    global captura
    #print(startRecord)
    startRecord = True
    strTime = time.strftime("%Y%m%d-%H%M%S")
    fr = 'dataset\\ds_' + strTime + '.avi'
    recordFile = rootDirDataset + fr
    cropped = roiZoom[rY+thicknessLine:rY+rH-thicknessLine, rX+thicknessLine:rX+rW-thicknessLine]
    cH, cW, cC = cropped.shape
    out = cv2.VideoWriter(recordFile,cv2.VideoWriter_fourcc(*'XVID'),int(originalFps),(cW,cH))
    out.write(cropped)
    #print("Writing in file out: ",actualFrame)
    fps = originalFps/2

def mouse(event,x,y,flags,params):
    global cv2, roiZoom, move_rectangle,pt1, pt2,color,rX, rY
    #print("Moused")
    if event == cv2.EVENT_LBUTTONDOWN:
        move_rectangle = True
        #print(move_rectangle)        
    if event == cv2.EVENT_MOUSEMOVE:
        if move_rectangle:
            #print("X: ", x, "Y: ", y)
            if x >= 0:
                rX = x
            else:
                rX = 0
            if y >= 0:
                rY = y
            else:
                rY = 0
            pt1 = (rX,rY)
            pt2 = (rX+rW, rY+rH)
            color = (0,0,255)
    if event == cv2.EVENT_LBUTTONUP:
        move_rectangle = False
        #print(move_rectangle)
        color = (0,255,0)

def nextVideo():
    global captura
    global length
    global fps
    global originalFps
    global fileList
    global numFileList
    print("Next Video is: ", fileList[numFileList])
    num = len(fileList)
    if numFileList == num - 1:
        print("End of List")
        sys.exit(1)

    #captura = cv2.VideoCapture(rootDir + fileList[numFileList])
    captura = cv2.VideoCapture(fileList[numFileList])
    length = int(captura.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = captura.get(cv2.CAP_PROP_FPS)
    originalFps = fps


#rootDir = 'C:\\tmp\PROJETO\\videos\\Amostragem de Evasões em Veículos\\HP\\'
rootDirVideos = 'C:\\Apps\\MESTRADO\\Videos\\4. Hp - Julho\\'
#rootDirVideos = 'C:\\Apps\\MESTRADO\\FAICON\\data\\production\\'
rootDirDataset = 'C:\\Apps\\MESTRADO\\Videos\\'

#fileList = os.listdir(rootDir)
fileList = glob.glob(rootDirVideos +'*.avi')
print("Found", len(fileList)," file(s) in this folder.")
numFileList = 0

for file in fileList:
    pass
    #print(file)
 
#captura = cv2.VideoCapture(rootDir + '13. Pular e passar por baixo da catraca.avi')
#length = int(captura.get(cv2.CAP_PROP_FRAME_COUNT))
#fps = captura.get(cv2.CAP_PROP_FPS)
#originalFps = fps

nextVideo()

record = False
startRecord = False
zoom = 1
printText = True

fileAnnotation = rootDirDataset + 'dataset\\' + 'dataset_3_classes.csv'

pause = 0

countRecordFrame = 0
countRecordFrameMax = 10

color = (0,255,0)

rX = 200*zoom
rY = 25*zoom
rW = 150*zoom
rH = 200*zoom
pt1 = (rX,rY)
pt2 = (rX+rW, rY+rH)

thicknessLine = 1

move_rectangle = False

out = cv2.VideoWriter()
k = 0

while(1):
    dataClassSimPulaCatraca = []
    dataClassNaoPulaCatraca = []
    dataClassSimPassouPorBaixo = []
    try:
        dataA = pd.read_csv(fileAnnotation,sep=';').to_dict(orient="row")
        dataClassSimPulaCatraca = []
        dataClassNaoPulaCatraca = []
        dataClassSimPassouPorBaixo = []
        for dataR in dataA:
            if dataR['class'] == 'NaoPulouCatraca':
                dataClassNaoPulaCatraca.append(dataR['file'])
            if dataR['class'] == 'SimPulouCatraca':
                dataClassSimPulaCatraca.append(dataR['file'])
            if dataR['class'] == 'SimPassouPorBaixo':
                dataClassSimPassouPorBaixo.append(dataR['file'])
    except:
        print("Ainda não há anotação...")
    #print("Anotacao - NAO Pulou Catraca", len(dataClassNaoPulaCatraca))
    #print("Anotacao - SIM Pulou Catraca", len(dataClassSimPulaCatraca))
    #print("-------------------------------------")
    #print("TOTAL: ",len(dataClassNaoPulaCatraca) + len(dataClassSimPulaCatraca))


    speedVideo = 1/fps
    if pause == 0:
        #time.sleep(speedVideo)
        ret, frame = captura.read()
        if not ret:
            #print("Go to Next video...")
            numFileList += 1
            nextVideo()
            ret, frame = captura.read()
       
    actualFrame = captura.get(cv2.CAP_PROP_POS_FRAMES)
    totalFrames = captura.get(cv2.CAP_PROP_FRAME_COUNT)

    height, width, channels = frame.shape

    roiZoom = frame
    if zoom>0:
        roiZoom = cv2.resize(frame, (width*zoom, height*zoom), interpolation=cv2.INTER_LANCZOS4)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,100)
    fontScale = 0.400*zoom
    fontColor = (0,255,0)
    lineType = 1
    newH, newW, newC = roiZoom.shape

    if printText:
        #text = 'FPS: ' + str(fps) + '('+ str(originalFps) + ')' + '\nFrame: ' + str(actualFrame) + "/" + str(totalFrames) + ' \nH: ' + str(newH) + ', W: ' + str(newW) + "\nFile: " + fileList[numFileList]
        text = 'FPS: ' + str(fps) + '('+ str(originalFps) + ')' + '\nFrame: ' + str(actualFrame) + "/" + str(totalFrames) + ' \nH: ' + str(newH) + ', W: ' + str(newW) + '\nFile: ' + str(numFileList) + '(' + str(len(fileList)) +  ')'
        if record:
            text += '\nREC'    
        for i, line in enumerate(text.split('\n')):
            cv2.putText(roiZoom,line,bottomLeftCornerOfText, font,fontScale, fontColor, lineType)
            bottomLeftCornerOfText = (10,bottomLeftCornerOfText[1] + 20)
        

    cv2.rectangle(roiZoom, pt1=pt1, pt2=pt2, color=color, thickness=thicknessLine, lineType=4) # Draw retangle on image..
    
    # TODO: Use a floating rectangle to assist in annotating the dataset.

    cv2.setMouseCallback('Video', mouse)

    cropped = roiZoom[rY+thicknessLine:rY+rH-thicknessLine, rX+thicknessLine:rX+rW-thicknessLine]
    cv2.imshow("Cropped", cropped)

    cv2.imshow("Video", roiZoom)
    #print(roiZoom.shape)

    if record:
        if startRecord:
            #global out
            #print(startRecord)
            out.write(cropped) 
            print("Writing in file out: ",actualFrame)            
            if countRecordFrame == countRecordFrameMax:
                startRecord = False
                record = False
                endFileRecord()
                countRecordFrame = 0
            countRecordFrame += 1
        else:
            startFileRecord()

        # Define the codec and create VideoWriter object
        # fourcc = cv2.VideoWriter_fourcc(*'XVID')
                
        #out.release()
    sleepTime = int(1/fps*1000)
    k = cv2.waitKey(sleepTime) & 0xff
    if k != 255:
        pass
        #print(k)
    if k == 27:
        break
    elif k == 32:
        #print(k)
        if pause == 1:
            pause = 0
        else:
            pause = 1
    elif k == 52:
        #NumPad #4
        #print(k)
        perFrames = 20
        if actualFrame > perFrames:
            captura.set(cv2.CAP_PROP_POS_FRAMES,actualFrame - perFrames)
            cv2.imshow("Video", roiZoom)
    elif k == 54:
        #NumPad #6
        #print(k)
        perFrames = 20
        if actualFrame < totalFrames:
            captura.set(cv2.CAP_PROP_POS_FRAMES,actualFrame + perFrames)
            cv2.imshow("Video", roiZoom)            
    elif k == 45:
        #NumPad (-)
        #print(k)
        if fps > 0:
            fps -= 1
    elif k == 43:
        #NumPad (+)
        #print(k)
        fps += 1
    elif k == 110:
        #n
        #print(k)
        numFileList += 1
        nextVideo()
    elif k == 112:
         #p
        #print(k)
        if numFileList == 0:
            pass
        else:
            numFileList -= 1
        nextVideo()
    elif k == 114:
        #R
        #print(k)
        if record:
            endFileRecord()
        else:
            record = True
captura.release()
cv2.destroyAllWindows()
