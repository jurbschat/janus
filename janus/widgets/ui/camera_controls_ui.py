# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camera_controls.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QWidgetCamera(object):
    def setupUi(self, QWidgetCamera):
        QWidgetCamera.setObjectName("QWidgetCamera")
        QWidgetCamera.resize(445, 136)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(QWidgetCamera.sizePolicy().hasHeightForWidth())
        QWidgetCamera.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(QWidgetCamera)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(QWidgetCamera)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.labelCameraGain = QtWidgets.QLabel(self.groupBox)
        self.labelCameraGain.setObjectName("labelCameraGain")
        self.gridLayout.addWidget(self.labelCameraGain, 0, 0, 1, 1)
        self.spinBoxCameraGain = QNoWheelSpinBox(self.groupBox)
        self.spinBoxCameraGain.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxCameraGain.setObjectName("spinBoxCameraGain")
        self.gridLayout.addWidget(self.spinBoxCameraGain, 0, 1, 1, 1)
        self.horizontalSliderCameraGain = QtWidgets.QSlider(self.groupBox)
        self.horizontalSliderCameraGain.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderCameraGain.setObjectName("horizontalSliderCameraGain")
        self.gridLayout.addWidget(self.horizontalSliderCameraGain, 0, 2, 1, 1)
        self.checkBoxCameraGainAuto = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxCameraGainAuto.setObjectName("checkBoxCameraGainAuto")
        self.gridLayout.addWidget(self.checkBoxCameraGainAuto, 0, 3, 1, 1)
        self.labelCameraExposureTime = QtWidgets.QLabel(self.groupBox)
        self.labelCameraExposureTime.setObjectName("labelCameraExposureTime")
        self.gridLayout.addWidget(self.labelCameraExposureTime, 1, 0, 1, 1)
        self.spinBoxCameraExposureTime = QNoWheelSpinBox(self.groupBox)
        self.spinBoxCameraExposureTime.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.spinBoxCameraExposureTime.setMinimum(1)
        self.spinBoxCameraExposureTime.setMaximum(1000000)
        self.spinBoxCameraExposureTime.setSingleStep(1000)
        self.spinBoxCameraExposureTime.setProperty("value", 10000)
        self.spinBoxCameraExposureTime.setObjectName("spinBoxCameraExposureTime")
        self.gridLayout.addWidget(self.spinBoxCameraExposureTime, 1, 1, 1, 1)
        self.horizontalSliderCameraExposureTime = QtWidgets.QSlider(self.groupBox)
        self.horizontalSliderCameraExposureTime.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSliderCameraExposureTime.setObjectName("horizontalSliderCameraExposureTime")
        self.gridLayout.addWidget(self.horizontalSliderCameraExposureTime, 1, 2, 1, 1)
        self.checkBoxCameraExposureTimeAuto = QtWidgets.QCheckBox(self.groupBox)
        self.checkBoxCameraExposureTimeAuto.setObjectName("checkBoxCameraExposureTimeAuto")
        self.gridLayout.addWidget(self.checkBoxCameraExposureTimeAuto, 1, 3, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(QWidgetCamera)
        QtCore.QMetaObject.connectSlotsByName(QWidgetCamera)

    def retranslateUi(self, QWidgetCamera):
        _translate = QtCore.QCoreApplication.translate
        QWidgetCamera.setWindowTitle(_translate("QWidgetCamera", "Form"))
        self.groupBox.setTitle(_translate("QWidgetCamera", "Camera Controls"))
        self.labelCameraGain.setText(_translate("QWidgetCamera", "Gain"))
        self.spinBoxCameraGain.setSuffix(_translate("QWidgetCamera", " db"))
        self.checkBoxCameraGainAuto.setText(_translate("QWidgetCamera", "auto"))
        self.labelCameraExposureTime.setText(_translate("QWidgetCamera", "Exposure time"))
        self.spinBoxCameraExposureTime.setSuffix(_translate("QWidgetCamera", " μs"))
        self.checkBoxCameraExposureTimeAuto.setText(_translate("QWidgetCamera", "auto"))

from janus.widgets.qt_modified import QNoWheelSpinBox
