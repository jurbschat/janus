# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'janus/widgets/ui/acq_xrf_parameters.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FormAcqXrf(object):
    def setupUi(self, FormAcqXrf):
        FormAcqXrf.setObjectName("FormAcqXrf")
        FormAcqXrf.resize(275, 300)
        self.formLayout = QtWidgets.QFormLayout(FormAcqXrf)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(FormAcqXrf)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.spinBoxAcqXrfEnergy = QtWidgets.QSpinBox(FormAcqXrf)
        self.spinBoxAcqXrfEnergy.setMaximum(40000)
        self.spinBoxAcqXrfEnergy.setObjectName("spinBoxAcqXrfEnergy")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spinBoxAcqXrfEnergy)
        self.checkBoxAcqXrfEnergy = QtWidgets.QCheckBox(FormAcqXrf)
        self.checkBoxAcqXrfEnergy.setObjectName("checkBoxAcqXrfEnergy")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.checkBoxAcqXrfEnergy)
        self.doubleSpinBoxAcqXrfTransmissiom = QtWidgets.QDoubleSpinBox(FormAcqXrf)
        self.doubleSpinBoxAcqXrfTransmissiom.setDecimals(4)
        self.doubleSpinBoxAcqXrfTransmissiom.setMaximum(100.0)
        self.doubleSpinBoxAcqXrfTransmissiom.setSingleStep(0.01)
        self.doubleSpinBoxAcqXrfTransmissiom.setProperty("value", 0.01)
        self.doubleSpinBoxAcqXrfTransmissiom.setObjectName("doubleSpinBoxAcqXrfTransmissiom")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxAcqXrfTransmissiom)
        self.checkBoxAcqXrfTransmission = QtWidgets.QCheckBox(FormAcqXrf)
        self.checkBoxAcqXrfTransmission.setObjectName("checkBoxAcqXrfTransmission")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.checkBoxAcqXrfTransmission)
        self.label_5 = QtWidgets.QLabel(FormAcqXrf)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.doubleSpinBoxAcqXrfInterval = QtWidgets.QDoubleSpinBox(FormAcqXrf)
        self.doubleSpinBoxAcqXrfInterval.setObjectName("doubleSpinBoxAcqXrfInterval")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.doubleSpinBoxAcqXrfInterval)
        self.label_4 = QtWidgets.QLabel(FormAcqXrf)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.spinBoxAcqXrfEnergyMin = QtWidgets.QSpinBox(FormAcqXrf)
        self.spinBoxAcqXrfEnergyMin.setObjectName("spinBoxAcqXrfEnergyMin")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.spinBoxAcqXrfEnergyMin)
        self.labelAcqXrfEnergyMin = QtWidgets.QLabel(FormAcqXrf)
        self.labelAcqXrfEnergyMin.setObjectName("labelAcqXrfEnergyMin")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.labelAcqXrfEnergyMin)
        self.spinBoxAcqXrfEnergyMax = QtWidgets.QSpinBox(FormAcqXrf)
        self.spinBoxAcqXrfEnergyMax.setObjectName("spinBoxAcqXrfEnergyMax")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.FieldRole, self.spinBoxAcqXrfEnergyMax)
        self.labelAcqXrfEnergyMax = QtWidgets.QLabel(FormAcqXrf)
        self.labelAcqXrfEnergyMax.setObjectName("labelAcqXrfEnergyMax")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.LabelRole, self.labelAcqXrfEnergyMax)

        self.retranslateUi(FormAcqXrf)
        QtCore.QMetaObject.connectSlotsByName(FormAcqXrf)

    def retranslateUi(self, FormAcqXrf):
        _translate = QtCore.QCoreApplication.translate
        FormAcqXrf.setWindowTitle(_translate("FormAcqXrf", "Form"))
        self.label.setText(_translate("FormAcqXrf", "Excitation Energy"))
        self.spinBoxAcqXrfEnergy.setSuffix(_translate("FormAcqXrf", " eV"))
        self.checkBoxAcqXrfEnergy.setText(_translate("FormAcqXrf", "use current"))
        self.doubleSpinBoxAcqXrfTransmissiom.setSuffix(_translate("FormAcqXrf", " %"))
        self.checkBoxAcqXrfTransmission.setText(_translate("FormAcqXrf", "use current"))
        self.label_5.setText(_translate("FormAcqXrf", "Transmission"))
        self.doubleSpinBoxAcqXrfInterval.setSuffix(_translate("FormAcqXrf", " s"))
        self.label_4.setText(_translate("FormAcqXrf", "Integration Time"))
        self.spinBoxAcqXrfEnergyMin.setSuffix(_translate("FormAcqXrf", " eV"))
        self.labelAcqXrfEnergyMin.setText(_translate("FormAcqXrf", "Minimum Energy"))
        self.spinBoxAcqXrfEnergyMax.setSuffix(_translate("FormAcqXrf", " eV"))
        self.labelAcqXrfEnergyMax.setText(_translate("FormAcqXrf", "Maximum Energy"))

