# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gridtoolbar.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_GridToolbar(object):
    def setupUi(self, GridToolbar):
        GridToolbar.setObjectName("GridToolbar")
        GridToolbar.resize(489, 56)
        self.verticalLayout = QtWidgets.QVBoxLayout(GridToolbar)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.toolbarFrame = QtWidgets.QFrame(GridToolbar)
        self.toolbarFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.toolbarFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.toolbarFrame.setObjectName("toolbarFrame")
        self.verticalLayout.addWidget(self.toolbarFrame)
        self.actionTest = QtWidgets.QAction(GridToolbar)
        self.actionTest.setObjectName("actionTest")

        self.retranslateUi(GridToolbar)
        QtCore.QMetaObject.connectSlotsByName(GridToolbar)

    def retranslateUi(self, GridToolbar):
        _translate = QtCore.QCoreApplication.translate
        GridToolbar.setWindowTitle(_translate("GridToolbar", "Form"))
        self.actionTest.setText(_translate("GridToolbar", "test"))
        self.actionTest.setToolTip(_translate("GridToolbar", "test"))

