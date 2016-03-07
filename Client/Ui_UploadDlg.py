# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Work\Python\PyAsio\Client\UploadDlg.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_UploadDlg(object):
    def setupUi(self, UploadDlg):
        UploadDlg.setObjectName("UploadDlg")
        UploadDlg.resize(344, 166)
        self.gridLayout_2 = QtWidgets.QGridLayout(UploadDlg)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.editServerAddress = QtWidgets.QLineEdit(UploadDlg)
        self.editServerAddress.setObjectName("editServerAddress")
        self.gridLayout.addWidget(self.editServerAddress, 0, 1, 1, 1)
        self.btnSelect = QtWidgets.QPushButton(UploadDlg)
        self.btnSelect.setObjectName("btnSelect")
        self.gridLayout.addWidget(self.btnSelect, 2, 0, 1, 2)
        self.lblServerAddress = QtWidgets.QLabel(UploadDlg)
        self.lblServerAddress.setObjectName("lblServerAddress")
        self.gridLayout.addWidget(self.lblServerAddress, 0, 0, 1, 1)
        self.btnStart = QtWidgets.QPushButton(UploadDlg)
        self.btnStart.setObjectName("btnStart")
        self.gridLayout.addWidget(self.btnStart, 5, 0, 1, 2)
        self.progressBar = QtWidgets.QProgressBar(UploadDlg)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.gridLayout.addWidget(self.progressBar, 6, 0, 1, 2)
        self.lblSelectFile = QtWidgets.QLabel(UploadDlg)
        self.lblSelectFile.setAlignment(QtCore.Qt.AlignCenter)
        self.lblSelectFile.setObjectName("lblSelectFile")
        self.gridLayout.addWidget(self.lblSelectFile, 3, 0, 1, 2)
        self.line = QtWidgets.QFrame(UploadDlg)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 1, 0, 1, 2)
        self.line_2 = QtWidgets.QFrame(UploadDlg)
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.gridLayout.addWidget(self.line_2, 4, 0, 1, 2)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.retranslateUi(UploadDlg)
        QtCore.QMetaObject.connectSlotsByName(UploadDlg)
        UploadDlg.setTabOrder(self.editServerAddress, self.btnSelect)
        UploadDlg.setTabOrder(self.btnSelect, self.btnStart)

    def retranslateUi(self, UploadDlg):
        _translate = QtCore.QCoreApplication.translate
        UploadDlg.setWindowTitle(_translate("UploadDlg", "File upload"))
        self.editServerAddress.setText(_translate("UploadDlg", "127.0.0.1"))
        self.btnSelect.setText(_translate("UploadDlg", "Select a file to upload ..."))
        self.lblServerAddress.setText(_translate("UploadDlg", "Server address:"))
        self.btnStart.setText(_translate("UploadDlg", "Start upload"))
        self.lblSelectFile.setText(_translate("UploadDlg", "No file was selected"))

