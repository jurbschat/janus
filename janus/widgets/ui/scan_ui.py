# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scan.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Scan(object):
    def setupUi(self, Scan):
        Scan.setObjectName("Scan")
        Scan.resize(133, 96)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Scan.sizePolicy().hasHeightForWidth())
        Scan.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(Scan)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(Scan)
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.startScan = QtWidgets.QPushButton(self.groupBox)
        self.startScan.setObjectName("startScan")
        self.gridLayout.addWidget(self.startScan, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(Scan)
        QtCore.QMetaObject.connectSlotsByName(Scan)

    def retranslateUi(self, Scan):
        _translate = QtCore.QCoreApplication.translate
        Scan.setWindowTitle(_translate("Scan", "Form"))
        self.groupBox.setTitle(_translate("Scan", "Scan Options"))
        self.startScan.setText(_translate("Scan", "Start Scan"))

