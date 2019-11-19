# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'beamprofile.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BeamProfile(object):
    def setupUi(self, BeamProfile):
        BeamProfile.setObjectName("BeamProfile")
        BeamProfile.resize(611, 96)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(BeamProfile.sizePolicy().hasHeightForWidth())
        BeamProfile.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(BeamProfile)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(BeamProfile)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.alignCenterButton = QtWidgets.QPushButton(self.groupBox)
        self.alignCenterButton.setObjectName("alignCenterButton")
        self.verticalLayout_2.addWidget(self.alignCenterButton)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(BeamProfile)
        QtCore.QMetaObject.connectSlotsByName(BeamProfile)

    def retranslateUi(self, BeamProfile):
        _translate = QtCore.QCoreApplication.translate
        BeamProfile.setWindowTitle(_translate("BeamProfile", "Form"))
        self.groupBox.setTitle(_translate("BeamProfile", "Beamprofile"))
        self.alignCenterButton.setText(_translate("BeamProfile", "Align To Center"))

