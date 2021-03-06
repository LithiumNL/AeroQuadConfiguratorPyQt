# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui

class MotorCommandPanel(object):
    def setupUi(self, motorCommand):
        motorCommand.setObjectName('MotorCommandPanel')
        motorCommand.resize(818, 418)
        self.gridLayout = QtGui.QGridLayout(motorCommand)
        self.gridLayout.setObjectName('gridLayout')
        self.sendButton = QtGui.QPushButton(motorCommand)
        self.sendButton.setObjectName('sendButton')
        self.gridLayout.addWidget(self.sendButton, 1, 0, 1, 1)
        self.clearButton = QtGui.QPushButton(motorCommand)
        self.clearButton.setObjectName('clearButton')
        self.gridLayout.addWidget(self.clearButton, 1, 1, 1, 1)
        self.motor_slider_widget = QtGui.QWidget()
        self.motor_slider_widget.setLayout(QtGui.QHBoxLayout())
        self.gridLayout.addWidget(self.motor_slider_widget, 0, 0, 1, 2)

        self.retranslateUi(motorCommand)
        QtCore.QMetaObject.connectSlotsByName(motorCommand)

    def retranslateUi(self, motorCommand):
        motorCommand.setWindowTitle(QtGui.QApplication.translate("motorCommand", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.sendButton.setText(QtGui.QApplication.translate("motorCommand", "Send Command", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("motorCommand", "Clear", None, QtGui.QApplication.UnicodeUTF8))

