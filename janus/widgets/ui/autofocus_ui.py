# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'autofocus.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Autofocus(object):
    def setupUi(self, Autofocus):
        Autofocus.setObjectName("Autofocus")
        Autofocus.resize(896, 526)
        self.verticalLayout = QtWidgets.QVBoxLayout(Autofocus)
        self.verticalLayout.setObjectName("verticalLayout")
        self.auto_focus_group = QtWidgets.QGroupBox(Autofocus)
        self.auto_focus_group.setObjectName("auto_focus_group")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.auto_focus_group)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.delaySlider = QtWidgets.QSlider(self.auto_focus_group)
        self.delaySlider.setMinimumSize(QtCore.QSize(100, 0))
        self.delaySlider.setMaximum(20)
        self.delaySlider.setPageStep(1)
        self.delaySlider.setProperty("value", 3)
        self.delaySlider.setOrientation(QtCore.Qt.Horizontal)
        self.delaySlider.setObjectName("delaySlider")
        self.horizontalLayout_2.addWidget(self.delaySlider)
        self.delayEdit = QtWidgets.QLineEdit(self.auto_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delayEdit.sizePolicy().hasHeightForWidth())
        self.delayEdit.setSizePolicy(sizePolicy)
        self.delayEdit.setMinimumSize(QtCore.QSize(50, 0))
        self.delayEdit.setObjectName("delayEdit")
        self.horizontalLayout_2.addWidget(self.delayEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 8, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.startFocus = QtWidgets.QPushButton(self.auto_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.startFocus.sizePolicy().hasHeightForWidth())
        self.startFocus.setSizePolicy(sizePolicy)
        self.startFocus.setMinimumSize(QtCore.QSize(0, 0))
        self.startFocus.setObjectName("startFocus")
        self.gridLayout_2.addWidget(self.startFocus, 0, 0, 1, 1)
        self.gridLayout.addLayout(self.gridLayout_2, 13, 1, 1, 1)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.goalSlider = QtWidgets.QSlider(self.auto_focus_group)
        self.goalSlider.setMinimumSize(QtCore.QSize(100, 0))
        self.goalSlider.setMaximum(1000)
        self.goalSlider.setSingleStep(10)
        self.goalSlider.setPageStep(100)
        self.goalSlider.setProperty("value", 800)
        self.goalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.goalSlider.setObjectName("goalSlider")
        self.horizontalLayout_3.addWidget(self.goalSlider)
        self.goalEdit = QtWidgets.QLineEdit(self.auto_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.goalEdit.sizePolicy().hasHeightForWidth())
        self.goalEdit.setSizePolicy(sizePolicy)
        self.goalEdit.setMinimumSize(QtCore.QSize(50, 0))
        self.goalEdit.setObjectName("goalEdit")
        self.horizontalLayout_3.addWidget(self.goalEdit)
        self.gridLayout.addLayout(self.horizontalLayout_3, 6, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 12, 1, 1, 1)
        self.quantisizerLabel = QtWidgets.QLabel(self.auto_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quantisizerLabel.sizePolicy().hasHeightForWidth())
        self.quantisizerLabel.setSizePolicy(sizePolicy)
        self.quantisizerLabel.setObjectName("quantisizerLabel")
        self.gridLayout.addWidget(self.quantisizerLabel, 5, 1, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.quantSlider = QtWidgets.QSlider(self.auto_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quantSlider.sizePolicy().hasHeightForWidth())
        self.quantSlider.setSizePolicy(sizePolicy)
        self.quantSlider.setMinimumSize(QtCore.QSize(100, 0))
        self.quantSlider.setMaximum(1000)
        self.quantSlider.setSingleStep(10)
        self.quantSlider.setPageStep(100)
        self.quantSlider.setProperty("value", 200)
        self.quantSlider.setOrientation(QtCore.Qt.Horizontal)
        self.quantSlider.setObjectName("quantSlider")
        self.horizontalLayout.addWidget(self.quantSlider)
        self.quantEdit = QtWidgets.QLineEdit(self.auto_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.quantEdit.sizePolicy().hasHeightForWidth())
        self.quantEdit.setSizePolicy(sizePolicy)
        self.quantEdit.setMinimumSize(QtCore.QSize(50, 0))
        self.quantEdit.setObjectName("quantEdit")
        self.horizontalLayout.addWidget(self.quantEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 0, 1, 1)
        self.goalLabel = QtWidgets.QLabel(self.auto_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.goalLabel.sizePolicy().hasHeightForWidth())
        self.goalLabel.setSizePolicy(sizePolicy)
        self.goalLabel.setObjectName("goalLabel")
        self.gridLayout.addWidget(self.goalLabel, 6, 1, 1, 1)
        self.delayLabel = QtWidgets.QLabel(self.auto_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.delayLabel.sizePolicy().hasHeightForWidth())
        self.delayLabel.setSizePolicy(sizePolicy)
        self.delayLabel.setObjectName("delayLabel")
        self.gridLayout.addWidget(self.delayLabel, 8, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.auto_focus_group)
        self.continuous_focus_group = QtWidgets.QGroupBox(Autofocus)
        self.continuous_focus_group.setObjectName("continuous_focus_group")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.continuous_focus_group)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_ll = QtWidgets.QLabel(self.continuous_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ll.sizePolicy().hasHeightForWidth())
        self.label_ll.setSizePolicy(sizePolicy)
        self.label_ll.setObjectName("label_ll")
        self.gridLayout_4.addWidget(self.label_ll, 4, 1, 1, 1)
        self.clear_all = QtWidgets.QPushButton(self.continuous_focus_group)
        self.clear_all.setObjectName("clear_all")
        self.gridLayout_4.addWidget(self.clear_all, 6, 2, 1, 1)
        self.clear_ur = QtWidgets.QPushButton(self.continuous_focus_group)
        self.clear_ur.setObjectName("clear_ur")
        self.gridLayout_4.addWidget(self.clear_ur, 1, 2, 1, 1)
        self.label_lr = QtWidgets.QLabel(self.continuous_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_lr.sizePolicy().hasHeightForWidth())
        self.label_lr.setSizePolicy(sizePolicy)
        self.label_lr.setObjectName("label_lr")
        self.gridLayout_4.addWidget(self.label_lr, 3, 1, 1, 1)
        self.button_ul = QtWidgets.QPushButton(self.continuous_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_ul.sizePolicy().hasHeightForWidth())
        self.button_ul.setSizePolicy(sizePolicy)
        self.button_ul.setObjectName("button_ul")
        self.gridLayout_4.addWidget(self.button_ul, 0, 0, 1, 1)
        self.clear_ul = QtWidgets.QPushButton(self.continuous_focus_group)
        self.clear_ul.setObjectName("clear_ul")
        self.gridLayout_4.addWidget(self.clear_ul, 0, 2, 1, 1)
        self.clear_ll = QtWidgets.QPushButton(self.continuous_focus_group)
        self.clear_ll.setObjectName("clear_ll")
        self.gridLayout_4.addWidget(self.clear_ll, 4, 2, 1, 1)
        self.label_ul = QtWidgets.QLabel(self.continuous_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ul.sizePolicy().hasHeightForWidth())
        self.label_ul.setSizePolicy(sizePolicy)
        self.label_ul.setObjectName("label_ul")
        self.gridLayout_4.addWidget(self.label_ul, 0, 1, 1, 1)
        self.checkbox_enable_continuous_focus = QtWidgets.QCheckBox(self.continuous_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkbox_enable_continuous_focus.sizePolicy().hasHeightForWidth())
        self.checkbox_enable_continuous_focus.setSizePolicy(sizePolicy)
        self.checkbox_enable_continuous_focus.setObjectName("checkbox_enable_continuous_focus")
        self.gridLayout_4.addWidget(self.checkbox_enable_continuous_focus, 6, 0, 1, 1)
        self.clear_lr = QtWidgets.QPushButton(self.continuous_focus_group)
        self.clear_lr.setObjectName("clear_lr")
        self.gridLayout_4.addWidget(self.clear_lr, 3, 2, 1, 1)
        self.button_ll = QtWidgets.QPushButton(self.continuous_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_ll.sizePolicy().hasHeightForWidth())
        self.button_ll.setSizePolicy(sizePolicy)
        self.button_ll.setObjectName("button_ll")
        self.gridLayout_4.addWidget(self.button_ll, 4, 0, 1, 1)
        self.button_lr = QtWidgets.QPushButton(self.continuous_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_lr.sizePolicy().hasHeightForWidth())
        self.button_lr.setSizePolicy(sizePolicy)
        self.button_lr.setObjectName("button_lr")
        self.gridLayout_4.addWidget(self.button_lr, 3, 0, 1, 1)
        self.label_ur = QtWidgets.QLabel(self.continuous_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_ur.sizePolicy().hasHeightForWidth())
        self.label_ur.setSizePolicy(sizePolicy)
        self.label_ur.setObjectName("label_ur")
        self.gridLayout_4.addWidget(self.label_ur, 1, 1, 1, 1)
        self.button_ur = QtWidgets.QPushButton(self.continuous_focus_group)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.button_ur.sizePolicy().hasHeightForWidth())
        self.button_ur.setSizePolicy(sizePolicy)
        self.button_ur.setObjectName("button_ur")
        self.gridLayout_4.addWidget(self.button_ur, 1, 0, 1, 1)
        self.label_error = QtWidgets.QLabel(self.continuous_focus_group)
        self.label_error.setText("")
        self.label_error.setObjectName("label_error")
        self.gridLayout_4.addWidget(self.label_error, 5, 0, 1, 3)
        self.verticalLayout.addWidget(self.continuous_focus_group)

        self.retranslateUi(Autofocus)
        QtCore.QMetaObject.connectSlotsByName(Autofocus)

    def retranslateUi(self, Autofocus):
        _translate = QtCore.QCoreApplication.translate
        Autofocus.setWindowTitle(_translate("Autofocus", "Form"))
        self.auto_focus_group.setTitle(_translate("Autofocus", "Autofocus"))
        self.delayEdit.setText(_translate("Autofocus", "3"))
        self.startFocus.setText(_translate("Autofocus", "Start Autofocus"))
        self.goalEdit.setText(_translate("Autofocus", "0.8"))
        self.quantisizerLabel.setToolTip(_translate("Autofocus", "This specifies what input change counts as signal change"))
        self.quantisizerLabel.setText(_translate("Autofocus", "Quanisizer Treshold"))
        self.quantEdit.setText(_translate("Autofocus", "0.2"))
        self.goalLabel.setToolTip(_translate("Autofocus", "The goal specifies what signal strength counts as \"focus reached\" (in % of the best signal seen)"))
        self.goalLabel.setText(_translate("Autofocus", "Goal Treshold"))
        self.delayLabel.setToolTip(_translate("Autofocus", "After every move we wait for the given frames. This allows the camera image to catch up to the current position."))
        self.delayLabel.setText(_translate("Autofocus", "Delay Frames"))
        self.continuous_focus_group.setTitle(_translate("Autofocus", "Continuous Focus"))
        self.label_ll.setText(_translate("Autofocus", "Empty"))
        self.clear_all.setText(_translate("Autofocus", "Clear All"))
        self.clear_ur.setText(_translate("Autofocus", "Clear"))
        self.label_lr.setText(_translate("Autofocus", "Empty"))
        self.button_ul.setText(_translate("Autofocus", "Upper Left"))
        self.clear_ul.setText(_translate("Autofocus", "Clear"))
        self.clear_ll.setText(_translate("Autofocus", "Clear"))
        self.label_ul.setText(_translate("Autofocus", "Empty"))
        self.checkbox_enable_continuous_focus.setText(_translate("Autofocus", "Continuous Focus"))
        self.clear_lr.setText(_translate("Autofocus", "Clear"))
        self.button_ll.setText(_translate("Autofocus", "Lower Left"))
        self.button_lr.setText(_translate("Autofocus", "Lower Right"))
        self.label_ur.setText(_translate("Autofocus", "Empty"))
        self.button_ur.setText(_translate("Autofocus", "Upper Right"))
