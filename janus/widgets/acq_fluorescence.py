'''
Created on Oct 14, 2019

@author: janmeyer
'''

from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget
from ..core import Object
from ..const import ChemicalElement

class AcqXrfParameters(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        from janus.widgets.ui.acq_xrf_parameters_ui import Ui_FormAcqXrf
        self.widget = QWidget(self.parent)
        self.ui = Ui_FormAcqXrf()
        self.ui.setupUi(self.widget)

    def connect_signals(self):
        pass


class AcqXanesParameters(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        from janus.widgets.ui.acq_xanes_parameters_ui import Ui_FormAcqXanes
        self.widget = QWidget(self.parent)
        self.ui = Ui_FormAcqXanes()
        self.ui.setupUi(self.widget)
        self.ui.labelAcqXanesVelocity.hide()
        self.ui.doubleSpinBoxAcqXanesVelocity.hide()
        self.ui.labelAcqXanesInterval.hide()
        self.ui.doubleSpinBoxAcqXanesInterval.hide()
        
    def connect_signals(self):
        self.ui.elementChooserAcqXanesElement.currentIndexChanged.connect( \
                self.update_element)
        self.ui.comboBoxAcqXanesEdge.currentIndexChanged.connect( \
                self.update_edge)

    def update_element(self, i):
        element = ChemicalElement(i)
        self.ui.comboBoxAcqXanesEdge.blockSignals(True)
        for i in range(int(self.ui.comboBoxAcqXanesEdge.count()), -1, -1):
            self.ui.comboBoxAcqXanesEdge.removeItem(i)
        self.ui.comboBoxAcqXanesEdge.addItem("please choose")
        if "k_edge" in element.__dict__:
            self.ui.comboBoxAcqXanesEdge.addItem( \
                    "K = {0} eV".format(element.k_edge))
        if "l1_edge" in element.__dict__:
            self.ui.comboBoxAcqXanesEdge.addItem( \
                    "L1 = {0} eV".format(element.l1_edge))
        if "l2_edge" in element.__dict__:
            self.ui.comboBoxAcqXanesEdge.addItem( \
                    "L2 = {0} eV".format(element.l2_edge))
        if "l3_edge" in element.__dict__:
            self.ui.comboBoxAcqXanesEdge.addItem( \
                    "L3 = {0} eV".format(element.l3_edge))
        self.ui.comboBoxAcqXanesEdge.blockSignals(False)
   
    def update_edge(self, i):
        element = ChemicalElement( \
                self.ui.elementChooserAcqXanesElement.currentIndex())
        if element is None:
            return
        edges = ["", "k_edge", "l1_edge", "l2_edge", "l3_edge"]
        edge = getattr(element, edges[i], None)
        if edge is None:
            return
        self.ui.spinBoxAcqXanesEnergyStart.setValue(edge-70)
        self.ui.spinBoxAcqXanesEnergyStop.setValue(edge+50)
        emission_lines = ["", "k_alpha1", "l_alpha1", "l_alpha1", "l_alpha1"]
        emission_line = getattr(element, emission_lines[i], None)
        if emission_line is None:
            return
        self.ui.spinBoxAcqXanesEmissionEnergy.setValue(emission_line)


class AcqRunParameters(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        from janus.widgets.ui.acq_run_parameters_ui import Ui_FormAcqRun
        self.widget = QWidget(self.parent)
        self.ui = Ui_FormAcqRun()
        self.ui.setupUi(self.widget)

    def connect_signals(self):
        pass
