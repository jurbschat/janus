# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'janus/widgets/ui/acq_xanes_parameters.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FormAcqXanes(object):
    def setupUi(self, FormAcqXanes):
        FormAcqXanes.setObjectName("FormAcqXanes")
        FormAcqXanes.resize(275, 480)
        self.formLayout = QtWidgets.QFormLayout(FormAcqXanes)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(FormAcqXanes)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.elementChooserAcqXanesElement = QElementChooser(FormAcqXanes)
        self.elementChooserAcqXanesElement.setObjectName("elementChooserAcqXanesElement")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.elementChooserAcqXanesElement)
        self.label_2 = QtWidgets.QLabel(FormAcqXanes)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.comboBoxAcqXanesEdge = QtWidgets.QComboBox(FormAcqXanes)
        self.comboBoxAcqXanesEdge.setObjectName("comboBoxAcqXanesEdge")
        self.comboBoxAcqXanesEdge.addItem("")
        self.comboBoxAcqXanesEdge.addItem("")
        self.comboBoxAcqXanesEdge.addItem("")
        self.comboBoxAcqXanesEdge.addItem("")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.comboBoxAcqXanesEdge)
        self.label_3 = QtWidgets.QLabel(FormAcqXanes)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.doubleSpinBoxAcqXanesTransmission = QtWidgets.QDoubleSpinBox(FormAcqXanes)
        self.doubleSpinBoxAcqXanesTransmission.setDecimals(4)
        self.doubleSpinBoxAcqXanesTransmission.setMaximum(100.0)
        self.doubleSpinBoxAcqXanesTransmission.setSingleStep(0.01)
        self.doubleSpinBoxAcqXanesTransmission.setProperty("value", 0.01)
        self.doubleSpinBoxAcqXanesTransmission.setObjectName("doubleSpinBoxAcqXanesTransmission")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxAcqXanesTransmission)
        self.checkBoxAcqXanesTransmission = QtWidgets.QCheckBox(FormAcqXanes)
        self.checkBoxAcqXanesTransmission.setObjectName("checkBoxAcqXanesTransmission")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.checkBoxAcqXanesTransmission)
        self.doubleSpinBoxAcqXanesVelocity = QtWidgets.QDoubleSpinBox(FormAcqXanes)
        self.doubleSpinBoxAcqXanesVelocity.setMinimum(0.1)
        self.doubleSpinBoxAcqXanesVelocity.setMaximum(4.0)
        self.doubleSpinBoxAcqXanesVelocity.setProperty("value", 1.0)
        self.doubleSpinBoxAcqXanesVelocity.setObjectName("doubleSpinBoxAcqXanesVelocity")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxAcqXanesVelocity)
        self.labelAcqXanesInterval = QtWidgets.QLabel(FormAcqXanes)
        self.labelAcqXanesInterval.setObjectName("labelAcqXanesInterval")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.labelAcqXanesInterval)
        self.doubleSpinBoxAcqXanesInterval = QtWidgets.QDoubleSpinBox(FormAcqXanes)
        self.doubleSpinBoxAcqXanesInterval.setMinimum(0.01)
        self.doubleSpinBoxAcqXanesInterval.setMaximum(10.0)
        self.doubleSpinBoxAcqXanesInterval.setSingleStep(0.1)
        self.doubleSpinBoxAcqXanesInterval.setProperty("value", 1.0)
        self.doubleSpinBoxAcqXanesInterval.setObjectName("doubleSpinBoxAcqXanesInterval")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxAcqXanesInterval)
        self.label_6 = QtWidgets.QLabel(FormAcqXanes)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.spinBoxAcqXanesEnergyStart = QtWidgets.QSpinBox(FormAcqXanes)
        self.spinBoxAcqXanesEnergyStart.setMaximum(40000)
        self.spinBoxAcqXanesEnergyStart.setProperty("value", 12000)
        self.spinBoxAcqXanesEnergyStart.setObjectName("spinBoxAcqXanesEnergyStart")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.spinBoxAcqXanesEnergyStart)
        self.label_7 = QtWidgets.QLabel(FormAcqXanes)
        self.label_7.setObjectName("label_7")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.spinBoxAcqXanesEnergyStop = QtWidgets.QSpinBox(FormAcqXanes)
        self.spinBoxAcqXanesEnergyStop.setMaximum(40000)
        self.spinBoxAcqXanesEnergyStop.setProperty("value", 12100)
        self.spinBoxAcqXanesEnergyStop.setObjectName("spinBoxAcqXanesEnergyStop")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.spinBoxAcqXanesEnergyStop)
        self.labelAcqXanesVelocity = QtWidgets.QLabel(FormAcqXanes)
        self.labelAcqXanesVelocity.setObjectName("labelAcqXanesVelocity")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.labelAcqXanesVelocity)
        self.spinBoxAcqXanesEmissionEnergy = QtWidgets.QSpinBox(FormAcqXanes)
        self.spinBoxAcqXanesEmissionEnergy.setMaximum(40000)
        self.spinBoxAcqXanesEmissionEnergy.setProperty("value", 11000)
        self.spinBoxAcqXanesEmissionEnergy.setObjectName("spinBoxAcqXanesEmissionEnergy")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.FieldRole, self.spinBoxAcqXanesEmissionEnergy)
        self.spinBoxAcqXrfRoiWidth = QtWidgets.QSpinBox(FormAcqXanes)
        self.spinBoxAcqXrfRoiWidth.setMaximum(500)
        self.spinBoxAcqXrfRoiWidth.setProperty("value", 10)
        self.spinBoxAcqXrfRoiWidth.setObjectName("spinBoxAcqXrfRoiWidth")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.FieldRole, self.spinBoxAcqXrfRoiWidth)
        self.label_8 = QtWidgets.QLabel(FormAcqXanes)
        self.label_8.setObjectName("label_8")
        self.formLayout.setWidget(8, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.label_9 = QtWidgets.QLabel(FormAcqXanes)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(9, QtWidgets.QFormLayout.LabelRole, self.label_9)

        self.retranslateUi(FormAcqXanes)
        QtCore.QMetaObject.connectSlotsByName(FormAcqXanes)

    def retranslateUi(self, FormAcqXanes):
        _translate = QtCore.QCoreApplication.translate
        FormAcqXanes.setWindowTitle(_translate("FormAcqXanes", "Form"))
        self.label.setText(_translate("FormAcqXanes", "Element"))
        self.label_2.setText(_translate("FormAcqXanes", "Edge"))
        self.comboBoxAcqXanesEdge.setItemText(0, _translate("FormAcqXanes", "K"))
        self.comboBoxAcqXanesEdge.setItemText(1, _translate("FormAcqXanes", "L1"))
        self.comboBoxAcqXanesEdge.setItemText(2, _translate("FormAcqXanes", "L2"))
        self.comboBoxAcqXanesEdge.setItemText(3, _translate("FormAcqXanes", "L3"))
        self.label_3.setText(_translate("FormAcqXanes", "Transmission"))
        self.doubleSpinBoxAcqXanesTransmission.setSuffix(_translate("FormAcqXanes", " %"))
        self.checkBoxAcqXanesTransmission.setText(_translate("FormAcqXanes", "use current"))
        self.doubleSpinBoxAcqXanesVelocity.setSuffix(_translate("FormAcqXanes", " eV/s"))
        self.labelAcqXanesInterval.setText(_translate("FormAcqXanes", "Integration time"))
        self.doubleSpinBoxAcqXanesInterval.setSuffix(_translate("FormAcqXanes", " s"))
        self.label_6.setText(_translate("FormAcqXanes", "Start Energy"))
        self.spinBoxAcqXanesEnergyStart.setSuffix(_translate("FormAcqXanes", " eV"))
        self.label_7.setText(_translate("FormAcqXanes", "Stop Energy"))
        self.spinBoxAcqXanesEnergyStop.setSuffix(_translate("FormAcqXanes", " eV"))
        self.labelAcqXanesVelocity.setText(_translate("FormAcqXanes", "Velocity"))
        self.spinBoxAcqXanesEmissionEnergy.setSuffix(_translate("FormAcqXanes", " eV"))
        self.spinBoxAcqXrfRoiWidth.setSuffix(_translate("FormAcqXanes", " eV"))
        self.spinBoxAcqXrfRoiWidth.setPrefix(_translate("FormAcqXanes", "+/- "))
        self.label_8.setText(_translate("FormAcqXanes", "Emission line"))
        self.label_9.setText(_translate("FormAcqXanes", "ROI width"))

from janus.widgets.qt_modified import QElementChooser
