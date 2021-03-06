'''
Created on 27 mrt. 2013

@author: Lithium
'''

import logging
from PyQt4 import QtCore, QtGui
from ui.subpanel.BasePanelController import BasePanelController
from ui.subpanel.receivercalibration.ReceiverCalibrationPanel import Ui_ReceiverCalibrationPanel


class ReceiverCalibrationController(QtGui.QWidget, BasePanelController):

    def __init__(self, vehicle_model, message_sender):
        
        QtGui.QWidget.__init__(self)
        BasePanelController.__init__(self)
        
        self.vehicle_model = vehicle_model
        self.message_sender = message_sender

        
        self.ui = Ui_ReceiverCalibrationPanel()
        self.ui.setupUi(self)
        self.ui.start.setEnabled(True)
        self.ui.cancel.setEnabled(False)
        
        leftStickScene = QtGui.QGraphicsScene()
        leftStickBackground = QtGui.QPixmap("./resources/TxDial.png")
        leftStickItem = QtGui.QGraphicsPixmapItem(leftStickBackground)
        leftStickScene.addItem(leftStickItem)
        self.leftStick = QtGui.QGraphicsEllipseItem(QtCore.QRectF(75, 75, 30, 30))
        self.leftStick.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern), 2))
        self.leftStick.setBrush(QtGui.QBrush(QtCore.Qt.blue, QtCore.Qt.SolidPattern))
        leftStickScene.addItem(self.leftStick)
        self.ui.leftTransmitter.setScene(leftStickScene)
        
        rightStickScene = QtGui.QGraphicsScene()
        rightStickBackground = QtGui.QPixmap("./resources/TxDial.png")
        rightStickItem = QtGui.QGraphicsPixmapItem(rightStickBackground)
        rightStickScene.addItem(rightStickItem)
        self.rightStick = QtGui.QGraphicsEllipseItem(QtCore.QRectF(75, 75, 30, 30))
        self.rightStick.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.black, QtCore.Qt.SolidPattern), 2))
        self.rightStick.setBrush(QtGui.QBrush(QtCore.Qt.blue, QtCore.Qt.SolidPattern))
        rightStickScene.addItem(self.rightStick)
        self.ui.rightTransmitter.setScene(rightStickScene)   
        
        self.running = False
        self.amount_channels = 12
        self.RCmin = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        self.RCmax = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
        self.max_amount_channels = 12
        
        self.ui.start.clicked.connect(self.start_RCcalibration)
        self.ui.cancel.clicked.connect(self.cancel_RCcalibration)

    def start(self, xmlSubPanel, boardConfiguration):
        self.xmlSubPanel = xmlSubPanel
        self.boardConfiguration = boardConfiguration
        try:
            self.amount_channels = int(self.boardConfiguration["Receiver Nb Channels"])
        except:
            logging.warning("Can't read amount of channels from boardconfiguration!")
        self.enable_gui_attribute()

    def start_RCcalibration(self):
        if self.running:    
            self.ui.start.setText("Start")
            self.cancel_RCcalibration() #we can stop the calibration it's done
            self.timer.stop()
            self.send_calibration_value()
        
        elif not self.running:
            if self.comm.isConnected() == True:
                self.comm.write("H")
                self.comm.write("t")
                self.timer = QtCore.QTimer()
                self.timer.timeout.connect(self.read_continuousData)
                self.timer.start(50)
                self.startCommThread()
                self.running = True
                
                self.ui.cancel.setEnabled(True)
                self.ui.next.setEnabled(False)
                
                self.ui.start.setText("Finish")
                
                self.RCmin = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
                self.RCmax = [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500]
                
    def cancel_RCcalibration(self):
        self.comm.write("x")
        self.timer.stop()
        self.comm.flushResponse()
        self.running = False
        self.ui.cancel.setEnabled(False)
        self.ui.next.setEnabled(True)
        self.ui.start.setText("Start")
        
    def read_continuousData(self):
        isConnected = self.comm.isConnected()
        if isConnected and not self.commData.empty():
            string = self.commData.get()
            string_out = string.split(',')
            if self.running:
                for i in range(0, self.amount_channels):
                    if int(string_out[i]) < self.RCmin[i]:  
                        self.RCmin[i] = int(string_out[i])
                    if int(string_out[i]) > self.RCmax[i]:  
                        self.RCmax[i] = int(string_out[i])
                    self.update_gui(i, string_out[i])                      
                    
            self.update_left_stick(int(string_out[3]), int(string_out[2]))
            self.update_right_stick(int(string_out[0]), int(string_out[1]))
            
    def update_gui(self, channel_number, value):
        if channel_number == 4:
            self.ui.progressBar_RCmode.setValue(int(value))
        if channel_number == 5:
            self.ui.progressBar_RCAux1.setValue(int(value))
        if channel_number == 6:
            self.ui.progressBar_RCAux2.setValue(int(value))
        if channel_number == 7:
            self.ui.progressBar_RCAux3.setValue(int(value))
        if channel_number == 8:
            self.ui.progressBar_RCAux4.setValue(int(value))
        if channel_number == 9:
            self.ui.progressBar_RCAux5.setValue(int(value))
        if channel_number == 10:
            self.ui.progressBar_RCAux6.setValue(int(value))
        if channel_number == 11:
            self.ui.progressBar_RCAux7.setValue(int(value))
    
    def update_left_stick(self, throttle, yaw):
        throttlePosition = self.scale(throttle, (1000.0, 2000.0), (58.0, -57.0))
        yawPosition = self.scale(yaw, (1000.0, 2000.0), (-57.0, 55.0))
        self.leftStick.setPos(yawPosition, throttlePosition)
        
    def update_right_stick(self, roll, pitch):
        rollPosition = self.scale(roll, (1000.0, 2000.0), (-57.0, 55.0))
        pitchPosition = self.scale(pitch, (1000.0, 2000.0), (58.0, -57.0))
        self.rightStick.setPos(rollPosition, pitchPosition)
    
    def scale(self, val, src, dst):
        return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]
    
    def enable_gui_attribute(self):
        for i in range(0, self.max_amount_channels):
            if i > (self.amount_channels - 1) and i == 5:
                self.ui.label_aux1.setHidden(True)
                self.ui.progressBar_RCAux1.setHidden(True)
            elif i > (self.amount_channels - 1) and i == 6:
                self.ui.label_aux2.setHidden(True)
                self.ui.progressBar_RCAux2.setHidden(True)
            elif i > (self.amount_channels - 1) and i == 7:
                self.ui.label_aux3.setHidden(True)
                self.ui.progressBar_RCAux3.setHidden(True)
            elif i > (self.amount_channels - 1) and i == 8:
                self.ui.label_aux4.setHidden(True)
                self.ui.progressBar_RCAux4.setHidden(True)
            elif i > (self.amount_channels - 1) and i == 9:
                self.ui.label_aux5.setHidden(True)
                self.ui.progressBar_RCAux5.setHidden(True)
            elif i > (self.amount_channels - 1) and i == 10:
                self.ui.label_aux6.setHidden(True)
                self.ui.progressBar_RCAux6.setHidden(True)
            elif i > (self.amount_channels - 1) and i == 11:
                self.ui.label_aux7.setHidden(True)
                self.ui.progressBar_RCAux7.setHidden(True)
    
    def send_calibration_value(self):
        self.comm.write("X");
        command = "G "
        for i in range(0, self.amount_channels):
            command += str(self.RCmin[i])
            command += ";"
            command += str(self.RCmax[i])
            command += ";"
            
        self.comm.write(command)    
        