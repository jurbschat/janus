# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'log.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_QWidgetLog(object):
    def setupUi(self, QWidgetLog):
        QWidgetLog.setObjectName("QWidgetLog")
        QWidgetLog.resize(626, 205)
        self.verticalLayout = QtWidgets.QVBoxLayout(QWidgetLog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(QWidgetLog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.groupBox)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(-1, 1, 9, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.labelLog = QtWidgets.QLabel(self.frame)
        self.labelLog.setObjectName("labelLog")
        self.horizontalLayout.addWidget(self.labelLog)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.comboBoxLogLevel = QtWidgets.QComboBox(self.frame)
        self.comboBoxLogLevel.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.comboBoxLogLevel.setObjectName("comboBoxLogLevel")
        self.comboBoxLogLevel.addItem("")
        self.comboBoxLogLevel.addItem("")
        self.comboBoxLogLevel.addItem("")
        self.comboBoxLogLevel.addItem("")
        self.comboBoxLogLevel.addItem("")
        self.horizontalLayout.addWidget(self.comboBoxLogLevel)
        self.pushButtonLogSave = QtWidgets.QPushButton(self.frame)
        self.pushButtonLogSave.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons:save.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButtonLogSave.setIcon(icon)
        self.pushButtonLogSave.setIconSize(QtCore.QSize(16, 16))
        self.pushButtonLogSave.setObjectName("pushButtonLogSave")
        self.horizontalLayout.addWidget(self.pushButtonLogSave)
        self.verticalLayout_2.addWidget(self.frame)
        self.textEditLog = QtWidgets.QTextEdit(self.groupBox)
        self.textEditLog.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        self.textEditLog.setReadOnly(True)
        self.textEditLog.setObjectName("textEditLog")
        self.verticalLayout_2.addWidget(self.textEditLog)
        self.verticalLayout.addWidget(self.groupBox)

        self.retranslateUi(QWidgetLog)
        self.comboBoxLogLevel.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(QWidgetLog)

    def retranslateUi(self, QWidgetLog):
        _translate = QtCore.QCoreApplication.translate
        QWidgetLog.setWindowTitle(_translate("QWidgetLog", "Form"))
        self.groupBox.setTitle(_translate("QWidgetLog", "Logging"))
        self.labelLog.setText(_translate("QWidgetLog", "Event Log"))
        self.comboBoxLogLevel.setItemText(0, _translate("QWidgetLog", "Debug"))
        self.comboBoxLogLevel.setItemText(1, _translate("QWidgetLog", "Info"))
        self.comboBoxLogLevel.setItemText(2, _translate("QWidgetLog", "Warning"))
        self.comboBoxLogLevel.setItemText(3, _translate("QWidgetLog", "Error"))
        self.comboBoxLogLevel.setItemText(4, _translate("QWidgetLog", "Critical"))

