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
    global originalFps
    record = False    
    startRecord = False
    out.release()
    print("Out released")
    fps = originalFps
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
    global originalFps
    global cropped
    global roiZoom
    print(startRecord)
    startRecord = True
    strTime = time.strftime("%Y%m%d-%H%M%S")
    fr = 'dataset\\ds_' + strTime + '.avi'
    recordFile = rootDir + fr
    out = cv2.VideoWriter(recordFile,cv2.VideoWriter_fourcc(*'XVID'),int(originalFps),(newW,newH))
    cropped = roiZoom[rY:rY+rH, rX:rX+rW]
    out.write(cropped)
    print("Writing in file out: ",actualFrame)
    fps = originalFps/2

def mouse(event,x,y,flags,params):
    global cv2, roiZoom, move_rectangle,pt1, pt2,color,rX, rY
    #print("Moused")
    if event == cv2.EVENT_LBUTTONDOWN:
        move_rectangle = True
        print(move_rectangle)        
    if event == cv2.EVENT_MOUSEMOVE:
        if move_rectangle:
            print("X: ", x, "Y: ", y)
            rX = x
            rY = y
            pt1 = (rX,rY)
            pt2 = (rX+rW, rY+rH)
            color = (0,0,255)
    if event == cv2.EVENT_LBUTTONUP:
        move_rectangle = False
        print(move_rectangle)
        color = (0,255,0)

rootDir = 'C:\\tmp\PROJETO\\videos\\Amostragem de Evasões em Veículos\\HP\\'
#rootDir = 'C:\\Apps\\MESTRADO\\Videos\\'
 
#captura = cv2.VideoCapture(0)
#captura = cv2.VideoCapture(rootDir + 'VR.7. Pular e passar por baixo da catraca.avi')
captura = cv2.VideoCapture(rootDir + '13. Pular e passar por baixo da catraca.avi')
length = int(captura.get(cv2.CAP_PROP_FRAME_COUNT))
fps = captura.get(cv2.CAP_PROP_FPS)
originalFps = fps
record = False
startRecord = False
zoom = 2
printText = False

fileAnnotation = rootDir + 'dataset\\' + 'dataset.csv'

pause = 0

countRecordFrame = 0
countRecordFrameMax = 10

color = (0,255,0)

rX = 400
rY = 50
rW = 300
rH = 400
pt1 = (rX,rY)
pt2 = (rX+rW, rY+rH)

move_rectangle = False

out = cv2.VideoWriter()
k = 0

while(1):
    speedVideo = 1/fps
    if pause == 0:
        #time.sleep(speedVideo)
        ret, frame = captura.read()
       
    actualFrame = captura.get(cv2.CAP_PROP_POS_FRAMES)

    height, width, channels = frame.shape

    roiZoom = frame
    roiZoom = cv2.resize(frame, (width*zoom, height*zoom), interpolation=cv2.INTER_LANCZOS4)

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

    cv2.rectangle(roiZoom, pt1=pt1, pt2=pt2, color=color, thickness=2, lineType=4) # Draw retangle on image..
    
    # TODO: Use a floating rectangle to assist in annotating the dataset.

    cv2.setMouseCallback('Video', mouse)

    cropped = roiZoom[rY:rY+rH, rX:rX+rW]
    cv2.imshow("Cropped", cropped)

    cv2.imshow("Video", roiZoom)
    #print(roiZoom.shape)

    if record:
        if startRecord:
            #global out
            print(startRecord)
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