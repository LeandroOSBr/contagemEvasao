# USE:
#   [ESC]: Exit
#   [SPACE BAR]: Pause
#   [NumPad #4]: Back any frames
#   [NumPad -]: Diminui FPS
#   [Num Pad +]: Aumenta FPS

import time
# Para facilitar escolha do item a ser anotado!
import tkinter as tk
import tkinter.ttk as ttk

import cv2

def endFileRecord():
    global record
    global startRecord
    global fps
    global out
    record = False    
    startRecord = False
    out.release()
    print("Out released")
    fps = fps*2
    a = open(fileAnnotation,"a") 
    response = input("Por favor, informe a classe: ")
    if response == 's':
        txtFile = '\nSimPulouCatraca' + ';' + fr
        a.write(txtFile)
        a.close
    elif response == 'n':
        txtFile = '\nNaoPulouCatraca' + ';' + fr
        a.write(txtFile)
        a.close

def startFileRecord():
    global startRecord
    global fr
    global recordFile
    global fps
    global out
    print(startRecord)
    startRecord = True
    strTime = time.strftime("%Y%m%d-%H%M%S")
    fr = 'dataset\\ds_' + strTime + '.avi'
    recordFile = rootDir + fr
    out = cv2.VideoWriter(recordFile,cv2.VideoWriter_fourcc(*'XVID'),int(originalFps),(newW,newH))
    out.write(roiZoom)
    print("Writing in file out: ",actualFrame)
    fps = fps/2

rootDir = 'C:\\tmp\PROJETO\\videos\\Amostragem de Evasões em Veículos\\HP\\'
#rootDir = 'C:\\Apps\\MESTRADO\\Videos\\'
 
#captura = cv2.VideoCapture(0)
#captura = cv2.VideoCapture(rootDir + 'VR.7. Pular e passar por baixo da catraca.avi')
captura = cv2.VideoCapture(rootDir + '9. Pular a catraca.avi')
length = int(captura.get(cv2.CAP_PROP_FRAME_COUNT))
fps = captura.get(cv2.CAP_PROP_FPS)
originalFps = fps
record = False
startRecord = False
zoom = 4
printText = False

fileAnnotation = rootDir + 'dataset\\' + 'dataset.csv'

pause = 0

countRecordFrame = 0
countRecordFrameMax = 10

out = cv2.VideoWriter()
k = 0

while(1):
    speedVideo = 1/fps
    if pause == 0:
        time.sleep(speedVideo)
        ret, frame = captura.read()
       
    actualFrame = captura.get(cv2.CAP_PROP_POS_FRAMES)

    height, width, channels = frame.shape
    cropSizeLRHeight = 1 - int(1 * height)
#    cropSizeLRHWidth = 1 - int(0.5 * width)
    cropSizeLRHWidth = 1 - int(0.4 * width)
    cropSizeRLHeight = int(0.75 * height) - 1
    cropSizeRLHWidth = int(0.95 * width) - 1
    roiCropped = frame[cropSizeLRHeight:cropSizeRLHeight, cropSizeLRHWidth:cropSizeRLHWidth]
    h, w, c = roiCropped.shape
    #zoom = cv2.resize(cropped, (h*4, w*4), interpolation = cv2.INTER_CUBIC)
    roiZoom = cv2.resize(roiCropped, (h*zoom, w*zoom), interpolation = cv2.INTER_LANCZOS4)

    font = cv2.FONT_HERSHEY_SIMPLEX
    bottomLeftCornerOfText = (10,10)
    fontScale = 0.125*zoom
    fontColor = (255,255,255)
    lineType = 0
    newH, newW, newC = roiZoom.shape

    if printText:
        text = 'FPS: ' + str(fps) + '('+ str(originalFps) + ')' + '\nActual Frame: ' + str(actualFrame) + ' \nH: ' + str(newH) + ', W: ' + str(newW)
        if record:
            text += '\nREC'    
        for i, line in enumerate(text.split('\n')):
            cv2.putText(roiZoom,line,bottomLeftCornerOfText, font,fontScale, fontColor, lineType)
            bottomLeftCornerOfText = (10,bottomLeftCornerOfText[1] + 30)

    # cv2.rectangle(roiZoom, (250,30), (450,200), (0,255,0), 5) # Draw retangle on image..
    # TODO: Use a floating rectangle to assist in annotating the dataset.
    cv2.imshow("Video", roiZoom)
    #print(roiZoom.shape)

    if record:
        if startRecord:
            #global out
            print(startRecord)
            out.write(roiZoom)
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
    
    k = cv2.waitKey(30) & 0xff
    print(k)
    if k == 27:
        break
    elif k == 32:
        print(k)
        if pause == 1:
            pause = 0
        else:
            pause = 1
    elif k == 52:
        #NumPad #4
        print(k)
        perFrames = 20
        if actualFrame > perFrames:
            captura.set(cv2.CAP_PROP_POS_FRAMES,actualFrame - perFrames)
            cv2.imshow("Video", roiZoom)
    elif k == 45:
        #NumPad (-)
        print(k)
        if fps > 0:
            fps -= 1
    elif k == 43:
        #NumPad (+)
        print(k)
        fps += 1
    elif k == 114:
        #R
        print(k)
        if record:
            endFileRecord()
        else:
            record = True
captura.release()
cv2.destroyAllWindows()