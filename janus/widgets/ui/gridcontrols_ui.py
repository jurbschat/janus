# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gridcontrols.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_GridControls(object):
    def setupUi(self, GridControls):
        GridControls.setObjectName("GridControls")
        GridControls.resize(578, 425)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GridControls.sizePolicy().hasHeightForWidth())
        GridControls.setSizePolicy(sizePolicy)
        GridControls.setMinimumSize(QtCore.QSize(0, 0))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(GridControls)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(GridControls)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.beamSize = QNoWheelDoubleSpinBox(self.groupBox)
        self.beamSize.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.beamSize.setPrefix("")
        self.beamSize.setMaximum(16777215.0)
        self.beamSize.setSingleStep(0.1)
        self.beamSize.setProperty("value", 10.0)
        self.beamSize.setObjectName("beamSize")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.beamSize)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.frame = QtWidgets.QFrame(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.beamOffsetX = QtWidgets.QDoubleSpinBox(self.frame)
        self.beamOffsetX.setMaximumSize(QtCore.QSize(16777215, 16777214))
        self.beamOffsetX.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.beamOffsetX.setMinimum(-16777215.0)
        self.beamOffsetX.setMaximum(16777215.0)
        self.beamOffsetX.setSingleStep(0.1)
        self.beamOffsetX.setObjectName("beamOffsetX")
        self.horizontalLayout.addWidget(self.beamOffsetX)
        self.beamOffsetY = QtWidgets.QDoubleSpinBox(self.frame)
        self.beamOffsetY.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.beamOffsetY.setMinimum(-16777215.0)
        self.beamOffsetY.setMaximum(16777215.0)
        self.beamOffsetY.setSingleStep(0.1)
        self.beamOffsetY.setProperty("value", 0.0)
        self.beamOffsetY.setObjectName("beamOffsetY")
        self.horizontalLayout.addWidget(self.beamOffsetY)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.frame)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.frame_5 = QtWidgets.QFrame(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.sampleOffsetX = QNoWheelDoubleSpinBox(self.frame_5)
        self.sampleOffsetX.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.sampleOffsetX.setMinimum(-16777215.0)
        self.sampleOffsetX.setMaximum(16777215.0)
        self.sampleOffsetX.setSingleStep(0.1)
        self.sampleOffsetX.setObjectName("sampleOffsetX")
        self.horizontalLayout_2.addWidget(self.sampleOffsetX)
        self.sampleOffsetY = QNoWheelDoubleSpinBox(self.frame_5)
        self.sampleOffsetY.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.sampleOffsetY.setMinimum(-16777215.0)
        self.sampleOffsetY.setMaximum(16777215.0)
        self.sampleOffsetY.setSingleStep(0.1)
        self.sampleOffsetY.setProperty("value", 0.0)
        self.sampleOffsetY.setObjectName("sampleOffsetY")
        self.horizontalLayout_2.addWidget(self.sampleOffsetY)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.frame_5)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(0, 0))
        self.label_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.frame_2 = QtWidgets.QFrame(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setLineWidth(1)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setHorizontalSpacing(6)
        self.gridLayout.setVerticalSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_3 = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setLineWidth(0)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.chipSelection = QtWidgets.QComboBox(self.frame_3)
        self.chipSelection.setMinimumSize(QtCore.QSize(0, 0))
        self.chipSelection.setMaximumSize(QtCore.QSize(270, 16777215))
        self.chipSelection.setObjectName("chipSelection")
        self.chipSelection.addItem("")
        self.chipSelection.addItem("")
        self.chipSelection.addItem("")
        self.verticalLayout_2.addWidget(self.chipSelection)
        self.gridLayout.addWidget(self.frame_3, 2, 0, 1, 1)
        self.chipInfoLabel = QtWidgets.QLabel(self.frame_2)
        self.chipInfoLabel.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.chipInfoLabel.setTextFormat(QtCore.Qt.RichText)
        self.chipInfoLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.chipInfoLabel.setObjectName("chipInfoLabel")
        self.gridLayout.addWidget(self.chipInfoLabel, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 2, 1, 1)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.frame_2)
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.frame_4 = QtWidgets.QFrame(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.chipOriginY = QNoWheelDoubleSpinBox(self.frame_4)
        self.chipOriginY.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.chipOriginY.setMinimum(-16777215.0)
        self.chipOriginY.setMaximum(16777215.0)
        self.chipOriginY.setSingleStep(0.1)
        self.chipOriginY.setProperty("value", 0.0)
        self.chipOriginY.setObjectName("chipOriginY")
        self.gridLayout_2.addWidget(self.chipOriginY, 0, 1, 1, 1)
        self.chipOriginX = QNoWheelDoubleSpinBox(self.frame_4)
        self.chipOriginX.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.chipOriginX.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.chipOriginX.setMinimum(-16777215.0)
        self.chipOriginX.setMaximum(16777215.0)
        self.chipOriginX.setSingleStep(0.1)
        self.chipOriginX.setObjectName("chipOriginX")
        self.gridLayout_2.addWidget(self.chipOriginX, 0, 0, 1, 1)
        self.saveUpdatedChipData = QtWidgets.QPushButton(self.frame_4)
        self.saveUpdatedChipData.setObjectName("saveUpdatedChipData")
        self.gridLayout_2.addWidget(self.saveUpdatedChipData, 1, 1, 1, 1)
        self.reset = QtWidgets.QPushButton(self.frame_4)
        self.reset.setObjectName("reset")
        self.gridLayout_2.addWidget(self.reset, 1, 0, 1, 1)
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.frame_4)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.fullWindowsOnly = QtWidgets.QCheckBox(self.groupBox)
        self.fullWindowsOnly.setText("")
        self.fullWindowsOnly.setObjectName("fullWindowsOnly")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.fullWindowsOnly)
        self.verticalLayout_3.addWidget(self.groupBox)

        self.retranslateUi(GridControls)
        QtCore.QMetaObject.connectSlotsByName(GridControls)

    def retranslateUi(self, GridControls):
        _translate = QtCore.QCoreApplication.translate
        GridControls.setWindowTitle(_translate("GridControls", "Form"))
        self.groupBox.setTitle(_translate("GridControls", "Grid Options"))
        self.label.setText(_translate("GridControls", "Beam size:"))
        self.beamSize.setSuffix(_translate("GridControls", " um"))
        self.label_2.setText(_translate("GridControls", "Beam offset:"))
        self.beamOffsetX.setPrefix(_translate("GridControls", "x: "))
        self.beamOffsetX.setSuffix(_translate("GridControls", " um"))
        self.beamOffsetY.setPrefix(_translate("GridControls", "y: "))
        self.beamOffsetY.setSuffix(_translate("GridControls", " um"))
        self.label_6.setText(_translate("GridControls", "Sample position:"))
        self.sampleOffsetX.setPrefix(_translate("GridControls", "x: "))
        self.sampleOffsetX.setSuffix(_translate("GridControls", " um"))
        self.sampleOffsetY.setPrefix(_translate("GridControls", "y: "))
        self.sampleOffsetY.setSuffix(_translate("GridControls", " um"))
        self.label_3.setText(_translate("GridControls", "Chip:"))
        self.chipSelection.setItemText(0, _translate("GridControls", "Chip A"))
        self.chipSelection.setItemText(1, _translate("GridControls", "Chip B"))
        self.chipSelection.setItemText(2, _translate("GridControls", "Chip C"))
        self.chipInfoLabel.setText(_translate("GridControls", "<html><head/><body><p><span style=\" color:#0800ff;\">info</span></p></body></html>"))
        self.label_5.setText(_translate("GridControls", "Chip Origin:"))
        self.chipOriginY.setPrefix(_translate("GridControls", "y: "))
        self.chipOriginY.setSuffix(_translate("GridControls", " um"))
        self.chipOriginX.setPrefix(_translate("GridControls", "x: "))
        self.chipOriginX.setSuffix(_translate("GridControls", " um"))
        self.saveUpdatedChipData.setText(_translate("GridControls", "Save to XML"))
        self.reset.setText(_translate("GridControls", "Reset Values"))
        self.label_4.setText(_translate("GridControls", "Full windows only"))
from janus.widgets.qt_modified import QNoWheelDoubleSpinBox
