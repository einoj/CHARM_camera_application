import numpy as np
import cv2
import sys
from PyQt4 import QtGui, QtCore

class Video():
    def __init__(self):
        self.record = False
        #Instansiate the three cameras
        self.cam1 = cv2.VideoCapture(0)
        self.cam2 = cv2.VideoCapture(1)
        self.cam3 = cv2.VideoCapture(2)

    def startCapture(self):
        self.capture = True
        while(self.capture):
            # Capture frame-by-frame
            self.ret, self.frame = self.cam1.read()
            self.ret2, self.frame2 =  self.cam2.read()
            self.ret3, self.frame3 =  self.cam3.read()
            # Display the resulting frame
            cv2.imshow('Camera 1',self.frame) 
            cv2.imshow('Camera 2',self.frame2)
            cv2.imshow('Camera 3',self.frame3)
            cv2.waitKey(5)

    def startRecording(self):
        #Define the codec and create VideoWriter oject        
        #fourcc = cv2.VideoWriter_fourcc(*'XVID')
        print "recording"
        fourcc = cv2.cv.CV_FOURCC(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 24.0, (640,480))
        self.record = True
        self.capture = False
        while (self.record):
            self.ret, self.frame = self.cam1.read()
            out.write(self.frame)
            cv2.imshow('Camera 1', self.frame)
            cv2.imshow('Camera 2',self.frame2)
            cv2.imshow('Camera 3',self.frame3)
            cv2.waitKey(5)
        self.capture = True

    def stopRecording(self):
       self.record = False 

    def quit(self):
        self.capture = False
        cap = self.cam1
        cv2.destroyAllWindows()
        cap.release()
        QtCore.QCoreApplication.quit()        

class Window(QtGui.QWidget):
    def __init__(self):

        QtGui.QWidget.__init__(self)
        self.setWindowTitle('Control Panel')

        self.capture = Video()

        self.start_record = QtGui.QPushButton('Record Cam 1',self)
        self.start_record.clicked.connect(self.buttonClicked)

        self.quit_button = QtGui.QPushButton('Quit',self)
        self.quit_button.clicked.connect(self.capture.quit)

        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.start_record)
        vbox.addWidget(self.quit_button)

        self.setLayout(vbox)
        self.setGeometry(100,100,200,200)
        self.show()
        self.capture.startCapture()

    def buttonClicked(self):
        sender = self.sender()
        if sender.text() == 'Record':
            sender.setText("Stop Recording")
            self.capture.startRecording()
        else:
            sender.setText('Record')
            self.capture.stopRecording()

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
