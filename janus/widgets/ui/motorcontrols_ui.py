# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'motorcontrols.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MotorControls(object):
    def setupUi(self, MotorControls):
        MotorControls.setObjectName("MotorControls")
        MotorControls.resize(443, 478)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MotorControls.sizePolicy().hasHeightForWidth())
        MotorControls.setSizePolicy(sizePolicy)
        MotorControls.setMinimumSize(QtCore.QSize(0, 478))
        self.verticalLayout = QtWidgets.QVBoxLayout(MotorControls)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(MotorControls)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setStyleSheet("")
        self.groupBox.setFlat(False)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_3.setMinimumSize(QtCore.QSize(159, 166))
        self.groupBox_3.setFlat(True)
        self.groupBox_3.setObjectName("groupBox_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_3)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.doubleSpinBox_7 = QNoWheelDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBox_7.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_7.setObjectName("doubleSpinBox_7")
        self.verticalLayout_3.addWidget(self.doubleSpinBox_7)
        self.doubleSpinBox_5 = QNoWheelDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBox_5.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_5.setObjectName("doubleSpinBox_5")
        self.verticalLayout_3.addWidget(self.doubleSpinBox_5)
        self.doubleSpinBox_6 = QNoWheelDoubleSpinBox(self.groupBox_3)
        self.doubleSpinBox_6.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_6.setObjectName("doubleSpinBox_6")
        self.verticalLayout_3.addWidget(self.doubleSpinBox_6)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.gridLayout_2.addWidget(self.groupBox_3, 2, 1, 1, 1)
        self.groupBox_5 = QtWidgets.QGroupBox(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setMinimumSize(QtCore.QSize(201, 248))
        self.groupBox_5.setFlat(True)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.doubleSpinBox_11 = QNoWheelDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_11.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_11.setMaximum(1000000.0)
        self.doubleSpinBox_11.setProperty("value", 2451.45)
        self.doubleSpinBox_11.setObjectName("doubleSpinBox_11")
        self.verticalLayout_5.addWidget(self.doubleSpinBox_11)
        self.doubleSpinBox_12 = QNoWheelDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_12.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_12.setObjectName("doubleSpinBox_12")
        self.verticalLayout_5.addWidget(self.doubleSpinBox_12)
        self.doubleSpinBox_13 = QNoWheelDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_13.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_13.setObjectName("doubleSpinBox_13")
        self.verticalLayout_5.addWidget(self.doubleSpinBox_13)
        self.doubleSpinBox_14 = QNoWheelDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_14.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_14.setObjectName("doubleSpinBox_14")
        self.verticalLayout_5.addWidget(self.doubleSpinBox_14)
        self.doubleSpinBox_15 = QNoWheelDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_15.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_15.setObjectName("doubleSpinBox_15")
        self.verticalLayout_5.addWidget(self.doubleSpinBox_15)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.gridLayout_2.addWidget(self.groupBox_5, 1, 1, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setMinimumSize(QtCore.QSize(171, 208))
        self.groupBox_2.setFlat(True)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout.setObjectName("gridLayout")
        self.doubleSpinBox = QNoWheelDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox.setMaximum(1000000.0)
        self.doubleSpinBox.setProperty("value", 25474.14)
        self.doubleSpinBox.setObjectName("doubleSpinBox")
        self.gridLayout.addWidget(self.doubleSpinBox, 0, 1, 1, 1)
        self.doubleSpinBox_2 = QNoWheelDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_2.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_2.setObjectName("doubleSpinBox_2")
        self.gridLayout.addWidget(self.doubleSpinBox_2, 1, 1, 1, 1)
        self.doubleSpinBox_3 = QNoWheelDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_3.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_3.setObjectName("doubleSpinBox_3")
        self.gridLayout.addWidget(self.doubleSpinBox_3, 2, 1, 1, 1)
        self.doubleSpinBox_4 = QNoWheelDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_4.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_4.setObjectName("doubleSpinBox_4")
        self.gridLayout.addWidget(self.doubleSpinBox_4, 3, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 4, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox_4 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_4.setMinimumSize(QtCore.QSize(159, 166))
        self.groupBox_4.setFlat(True)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.doubleSpinBox_8 = QNoWheelDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_8.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_8.setObjectName("doubleSpinBox_8")
        self.verticalLayout_4.addWidget(self.doubleSpinBox_8)
        self.doubleSpinBox_9 = QNoWheelDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_9.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_9.setObjectName("doubleSpinBox_9")
        self.verticalLayout_4.addWidget(self.doubleSpinBox_9)
        self.doubleSpinBox_10 = QNoWheelDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_10.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.doubleSpinBox_10.setObjectName("doubleSpinBox_10")
        self.verticalLayout_4.addWidget(self.doubleSpinBox_10)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem3)
        self.gridLayout_2.addWidget(self.groupBox_4, 2, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(MotorControls)
        QtCore.QMetaObject.connectSlotsByName(MotorControls)

    def retranslateUi(self, MotorControls):
        _translate = QtCore.QCoreApplication.translate
        MotorControls.setWindowTitle(_translate("MotorControls", "Form"))
        self.groupBox.setTitle(_translate("MotorControls", "Motor Controls"))
        self.groupBox_3.setTitle(_translate("MotorControls", "Centering Stage"))
        self.doubleSpinBox_7.setPrefix(_translate("MotorControls", "x: "))
        self.doubleSpinBox_7.setSuffix(_translate("MotorControls", " um"))
        self.doubleSpinBox_5.setPrefix(_translate("MotorControls", "y: "))
        self.doubleSpinBox_5.setSuffix(_translate("MotorControls", " um"))
        self.doubleSpinBox_6.setPrefix(_translate("MotorControls", "z: "))
        self.doubleSpinBox_6.setSuffix(_translate("MotorControls", " um"))
        self.groupBox_5.setTitle(_translate("MotorControls", "Beamstop"))
        self.doubleSpinBox_11.setPrefix(_translate("MotorControls", "front x: "))
        self.doubleSpinBox_11.setSuffix(_translate("MotorControls", " um"))
        self.doubleSpinBox_12.setPrefix(_translate("MotorControls", "front y: "))
        self.doubleSpinBox_12.setSuffix(_translate("MotorControls", " um"))
        self.doubleSpinBox_13.setPrefix(_translate("MotorControls", "all x: "))
        self.doubleSpinBox_13.setSuffix(_translate("MotorControls", " um"))
        self.doubleSpinBox_14.setPrefix(_translate("MotorControls", "all y: "))
        self.doubleSpinBox_15.setPrefix(_translate("MotorControls", "all z: "))
        self.groupBox_2.setTitle(_translate("MotorControls", "Gonio"))
        self.doubleSpinBox.setPrefix(_translate("MotorControls", "x: "))
        self.doubleSpinBox.setSuffix(_translate("MotorControls", " um"))
        self.doubleSpinBox_2.setPrefix(_translate("MotorControls", "y: "))
        self.doubleSpinBox_2.setSuffix(_translate("MotorControls", " um"))
        self.doubleSpinBox_3.setPrefix(_translate("MotorControls", "z: "))
        self.doubleSpinBox_3.setSuffix(_translate("MotorControls", " um"))
        self.doubleSpinBox_4.setPrefix(_translate("MotorControls", "r: "))
        self.doubleSpinBox_4.setSuffix(_translate("MotorControls", " deg"))
        self.groupBox_4.setTitle(_translate("MotorControls", "Onaxis"))
        self.doubleSpinBox_8.setPrefix(_translate("MotorControls", "x: "))
        self.doubleSpinBox_8.setSuffix(_translate("MotorControls", " um"))
        self.doubleSpinBox_9.setPrefix(_translate("MotorControls", "y: "))
        self.doubleSpinBox_9.setSuffix(_translate("MotorControls", " um"))
        self.doubleSpinBox_10.setPrefix(_translate("MotorControls", "z: "))
        self.doubleSpinBox_10.setSuffix(_translate("MotorControls", " um"))

from janus.widgets.qt_modified import QNoWheelDoubleSpinBox
