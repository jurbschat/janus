# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autofocus.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Autofocus(object):
    def setupUi(self, Autofocus):
        Autofocus.setObjectName("Autofocus")
        Autofocus.resize(178, 97)
        Autofocus.setMinimumSize(QtCore.QSize(178, 97))
        self.verticalLayout = QtWidgets.QVBoxLayout(Autofocus)
        self.verticalLayout.setObjectName("verticalLayout")
        self.focusGroup = QtWidgets.QGroupBox(Autofocus)
        self.focusGroup.setObjectName("focusGroup")
        self.gridLayout = QtWidgets.QGridLayout(self.focusGroup)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 0, 1, 1)
        self.startFocus = QtWidgets.QPushButton(self.focusGroup)
        self.startFocus.setMinimumSize(QtCore.QSize(115, 34))
        self.startFocus.setObjectName("startFocus")
        self.gridLayout.addWidget(self.startFocus, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 2, 1, 1)
        self.verticalLayout.addWidget(self.focusGroup)

        self.retranslateUi(Autofocus)
        QtCore.QMetaObject.connectSlotsByName(Autofocus)

    def retranslateUi(self, Autofocus):
        _translate = QtCore.QCoreApplication.translate
        Autofocus.setWindowTitle(_translate("Autofocus", "Form"))
        self.focusGroup.setTitle(_translate("Autofocus", "Autofocus"))
        self.startFocus.setText(_translate("Autofocus", "Start Autofocus"))

