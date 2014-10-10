import numpy as np
import cv2
import sys
from PyQt4 import QtGui, QtCore

class Video():
    def __init__(self):
        self.record1 = False
        self.record2 = False
        self.record3 = False
        self.recording = False
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
            cv2.waitKey(30)

    def startRecording(self):
        #Define the codec and create VideoWriter oject        
        #fourcc = cv2.VideoWriter_fourcc(*'XVID')
        if self.recording:
            #only start one instance of startRecording()
            #Which camera stream is recorded can be set by
            #the self.record variables
            print "already recording"
        else:
            self.recording = True
            fourcc = cv2.cv.CV_FOURCC(*'XVID')
            self.out1 = cv2.VideoWriter('output1.avi', fourcc, 33.0, (640,480))
            self.out2 = cv2.VideoWriter('output2.avi', fourcc, 33.0, (640,480))
            self.out3 = cv2.VideoWriter('output3.avi', fourcc, 33.0, (640,480))
            self.capture = False
            while (self.record1 or self.record2 or self.record3):
                self.ret, self.frame = self.cam1.read()
                self.ret2, self.frame2 =  self.cam2.read()
                self.ret3, self.frame3 =  self.cam3.read()
                if self.record1:
                    self.out1.write(self.frame)
                if  self.record2:
                    self.out2.write(self.frame2)
                if  self.record3:
                    self.out3.write(self.frame3)
                cv2.imshow('Camera 1', self.frame)
                cv2.imshow('Camera 2',self.frame2)
                cv2.imshow('Camera 3',self.frame3)
                cv2.waitKey(30)
            self.capture = True
            self.recording = False

    def stopRecording(self,a):
        if a == 1:
            self.record1 = False
            self.out1.release()
        if a == 2:
            self.record2 = False
            self.out2.release()
        if a == 3:
            self.record3 = False
            self.out3.release()
        if a == 4:
            self.record1 = False
            self.record2 = False
            self.record3 = False
            self.out3.release()
            self.out2.release()
            self.out1.release()

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

        self.start_record1 = QtGui.QPushButton('Record Cam 1',self)
        self.start_record1.clicked.connect(self.record1)

        self.start_record2 = QtGui.QPushButton('Record Cam 2',self)
        self.start_record2.clicked.connect(self.record2)

        self.start_record3 = QtGui.QPushButton('Record Cam 3',self)
        self.start_record3.clicked.connect(self.record3)

        self.start_recordAll = QtGui.QPushButton('Record All',self)
        self.start_recordAll.clicked.connect(self.recordAll)

        self.quit_button = QtGui.QPushButton('Quit',self)
        self.quit_button.clicked.connect(self.capture.quit)

        vbox = QtGui.QVBoxLayout(self)
        vbox.addWidget(self.start_record1)
        vbox.addWidget(self.start_record2)
        vbox.addWidget(self.start_record3)
        vbox.addWidget(self.start_recordAll)
        vbox.addWidget(self.quit_button)

        self.setLayout(vbox)
        self.setGeometry(100,100,200,200)
        self.show()
        self.capture.startCapture()

    def record1(self):
        sender = self.sender()
        if sender.text() == 'Record cam 1':
            sender.setText("Stop Recording cam 1")
            self.capture.record1 = True
            self.capture.startRecording()
        else:
            sender.setText('Record cam 1')
            self.capture.stopRecording(1)

    def record2(self):
        sender = self.sender()
        if sender.text() == 'Record cam 2':
            sender.setText("Stop Recording cam 2")
            self.capture.record2 = True
            self.capture.startRecording()
        else:
            sender.setText('Record cam 2')
            self.capture.stopRecording(2)

    def record3(self):
        sender = self.sender()
        if sender.text() == 'Record cam 3':
            sender.setText("Stop Recording cam 3")
            self.capture.record3 = True
            self.capture.startRecording()
        else:
            sender.setText('Record cam 3')
            self.capture.stopRecording(3)

    def recordAll(self):
        sender = self.sender()
        if sender.text() == 'Record All':
            self.capture.record1 = True
            self.capture.record2 = True
            self.capture.record3 = True
            sender.setText("Stop Recording All")
            self.start_record1.setText("Stop Recording cam 1")
            self.start_record2.setText("Stop Recording cam 2")
            self.start_record3.setText("Stop Recording cam 3")
            self.capture.startRecording()
        else:
            sender.setText('Record All')
            self.start_record1.setText("Record cam 1")
            self.start_record2.setText("Record cam 2")
            self.start_record3.setText("Record cam 3")
            self.capture.stopRecording(4)

if __name__ == '__main__':

    import sys
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
