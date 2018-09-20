import sys
import cv2
import os.path
import time

from PyQt5.QtCore import QTimer, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.uic import loadUi

rootDir = os.path.abspath(os.path.dirname(__file__))
 
record = False
startRecord = False
zoom = 1
printText = True

fileAnnotation = rootDir + 'dataset\\' + 'dataset.csv'

pause = 0


class CaptureDevice(QDialog):

    def __init__(self):
        super(CaptureDevice, self).__init__()
        uiFile = rootDir + '\\CaptureDevice.ui'
        loadUi(uiFile, self)

        # Variaveis
        self.timer = QTimer(self)
        #self.imagem = None

        # Declara Buttons
        self.btnCam.clicked.connect(self.start_stop_webcam)
        self.btnPlay.clicked.connect(self.videoPlay)
        self.btnPause.clicked.connect(self.videoPause)
        self.btnNextFrame.clicked.connect(self.videoNextFrame)
        self.btnNextFrames.clicked.connect(self.videoNextFrames)
        self.btnPreviusFrame.clicked.connect(self.videoPreviusFrame)
        self.btnPreviusFrames.clicked.connect(self.videoPreviusFrames)

    def start_stop_webcam(self):

        if self.btnCam.text() == "START CAM":
            #self.capture = cv2.VideoCapture(0)
            #self.capture = cv2.VideoCapture('C:\\Apps\\MESTRADO\\Videos\\HP.9. Pular a catraca.avi')
            self.capture = cv2.VideoCapture(self.openFileNameDialog())
            #self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            #self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self.length = int(self.capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.fps = self.capture.get(cv2.CAP_PROP_FPS)
            self.originalFps = self.fps
            self.speedVideo = 1/self.fps

            

            self.start_time()
            self.btnCam.setText("STOP CAM")
        else:
            self.btnCam.setText("START CAM")
            self.timer.stop()

    def start_time(self):
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)

    def update_frame(self):
        
        if pause == 0:
            self.txtInfoSpeed.setPlainText("Speed per Frame: " + str(self.speedVideo))
            time.sleep(self.speedVideo)
            self.ret, self.imagemCap = self.capture.read()
            self.txeInfoFrame.append("Frame # " + str(self.capture.get(cv2.CAP_PROP_POS_FRAMES)))

            self.btnPause.setStyleSheet("background-color: #e3e3e3")
        else:
            self.btnPause.setStyleSheet("background-color: blue")  

        self.actualFrame = self.capture.get(cv2.CAP_PROP_POS_FRAMES)        
        self.height, self.width, self.channels = self.imagemCap.shape
        self.cropSizeLRHeight = 1 - int(1 * self.height)
        self.cropSizeLRHWidth = 1 - int(0.4 * self.width)
        self.cropSizeRLHeight = int(0.85 * self.height) - 1
        self.cropSizeRLHWidth = int(1 * self.width) - 1
        self.roiCropped = self.imagemCap[self.cropSizeLRHeight:self.cropSizeRLHeight, self.cropSizeLRHWidth:self.cropSizeRLHWidth]
        self.h, self.w, self.c = self.roiCropped.shape
        #zoom = cv2.resize(cropped, (h*4, w*4), interpolation = cv2.INTER_CUBIC)
        self.roiZoom = cv2.resize(self.roiCropped, (self.h*zoom, self.w*zoom), interpolation = cv2.INTER_LANCZOS4)

        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (10,10)
        self.fontScale = 0.125*zoom
        self.fontColor = (255,255,255)
        self.lineType = 0
        self.newH, self.newW, self.newC = self.roiZoom.shape

        text = ''
        if printText:
            text = 'FPS: ' + str(self.fps) + '('+ str(self.originalFps) + ')' + '\nActual Frame: ' + str(self.actualFrame) + '/' + str(self.length) + ' \nH: ' + str(self.newH) + ', W: ' + str(self.newW)
        if record:
            text += '\nREC'    
        #for i, line in enumerate(text.split('\n')):
            #cv2.putText(self.roiZoom,line,self.bottomLeftCornerOfText, self.font,self.fontScale, self.fontColor, self.lineType)
            #self.bottomLeftCornerOfText = (10,self.bottomLeftCornerOfText[1] + 30)


        #self.txtInfoVideo.insertPlainText(text)
        self.txtInfoVideo.setPlainText(text)




        if self.ret == True:

            if self.checkEixoX.isChecked():
                self.limited_area()

            self.set_display_image(self.roiZoom)
            #cv2.imshow("Video", self.roiZoom)

    def set_display_image(self, framed):

        qtimg = QImage.Format_Indexed8

        if len(framed.shape) == 3:  # rows, cols, chanels
            if (framed.shape[2]) == 4:  # chanels == RGBA
                qtimg = QImage.Format_RGBA888
            else:
                qtimg = QImage.Format_RGB888

        tmp = QImage(framed, framed.shape[1], framed.shape[0], framed.strides[0],
                     qtimg)
        tmp = tmp.rgbSwapped()

        #self.lbFrames.setPixmap(QPixmap.fromImage(tmp))
        #self.lbFrames.setScaledContents(True)
        self.lbImagem.setPixmap(QPixmap.fromImage(tmp))
        self.lbImagem.setScaledContents(True)

    def openFileNameDialog(self):    
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Video Files (*.avi)", options=options)
        if fileName:
            print(fileName)
        return fileName

    def videoPlay(self):
        print("Play Press")


    def videoPause(self):
        global pause
        print("videoPause")
        if pause == 1:
            pause = 0            
        else:
            pause = 1            

    def videoNextFrame(self):
        print("videoNextFrame")

    def videoNextFrames(self):
        print("videoNextFrames")

    def videoPreviusFrame(self):
        print("videoPreviusFrame")

    def videoPreviusFrames(self):
        print("videoPreviusFrames")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = CaptureDevice()
    janela.show()
    sys.exit(app.exec_())

    k = cv2.waitKey(30) & 0xff
    print(k)
    if k == 27:
        #break
        sys.exit(app.exec_())
    elif k == 32:
        print(k)
        if pause == 1:
            pause = 0
        else:
            pause = 1
    elif k == 52:
        #NumPad #4
        print(k)
        perFrames = 40
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
            record = False
            startRecord = False
            out.release()
            print("Out released")
            fps = fps*2
            a = open(fileAnnotation,"a") 
            response = input("Por favor, informe a classe: ")
            txtFile = 'Pula-Catraca' + ';' + fr
            a.write(txtFile)
            a.close
        else:
            record = True