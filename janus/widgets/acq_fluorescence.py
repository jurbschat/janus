"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-BMX, FS-Petra-D, P11"
__license__ = "GPL"


from PyQt5.QtCore import QObject, Qt
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, \
        QHeaderView, QAbstractItemView
from ..core import Object
from ..const import ChemicalElement

class AcqXrfParameters(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.register_persistents()
        self.connect_signals()

    def setup_ui(self):
        from janus.widgets.ui.acq_xrf_parameters_ui import Ui_FormAcqXrf
        self.widget = QWidget(self.parent)
        self.ui = Ui_FormAcqXrf()
        self.ui.setupUi(self.widget)
        self.ui.labelAcqXrfEnergyMin.hide()
        self.ui.spinBoxAcqXrfEnergyMin.hide()
        self.ui.labelAcqXrfEnergyMax.hide()
        self.ui.spinBoxAcqXrfEnergyMax.hide()

    def connect_signals(self):
        pass

    def register_persistents(self):
        self.janus.utils["config"].add_persistent( \
                "acq_xrf", "energy", self.ui.spinBoxAcqXrfEnergy.value,
                self.ui.spinBoxAcqXrfEnergy.setValue, int)
        self.janus.utils["config"].add_persistent( \
                "acq_xrf", "energy_current", self.ui.checkBoxAcqXrfEnergy.isChecked,
                self.ui.checkBoxAcqXrfEnergy.setChecked, bool)
        self.janus.utils["config"].add_persistent( \
                "acq_xrf", "transmission", self.ui.doubleSpinBoxAcqXrfTransmissiom.value,
                self.ui.doubleSpinBoxAcqXrfTransmissiom.setValue, float)
        self.janus.utils["config"].add_persistent( \
                "acq_xrf", "transmission_current", self.ui.checkBoxAcqXrfTransmission.isChecked,
                self.ui.checkBoxAcqXrfTransmission.setChecked, bool)
        self.janus.utils["config"].add_persistent( \
                "acq_xrf", "integration_time", self.ui.doubleSpinBoxAcqXrfInterval.value,
                self.ui.doubleSpinBoxAcqXrfInterval.setValue, float)


class AcqXrfElementsTable(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.connect_signals()

    def setup_ui(self):
        self.widget = QTableWidget(0, 11, self.parent)
        header = ("Z", "Sym", "Name", "Kα1", "Kα2", "Kβ1", "Lα1", "Lα2", "Lβ1",
                "Lβ2", "Lγ1")
        self.widget.setHorizontalHeaderLabels(header)
        self.widget.verticalHeader().setVisible(False)
        self.widget.horizontalHeader().setHighlightSections(False)
        self.widget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.widget.horizontalHeader().setResizeMode(0, QHeaderView.ResizeToContents)
        self.widget.horizontalHeader().setResizeMode(1, QHeaderView.ResizeToContents)
        self.widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.hide()

    def connect_signals(self):
        pass

    def add_element_row(self, element):
        row = self.widget.rowCount()
        self.widget.setRowCount(row + 1)
        keys = ["z", "symbol", "name", "k_alpha1", "k_alpha2", "k_beta1",
                "l_alpha1", "l_alpha2", "l_beta1", "l_beta2", "l_gamma1"]
        if isinstance(element, int):
            element = ChemicalElement(element)
        column = 0
        for key in keys:
            text = ""
            if key in element.__dict__:
                text = str(element.__dict__[key])
            item = QTableWidgetItem(text)
            item.setFlags((Qt.ItemIsEnabled | Qt.ItemIsSelectable))
            self.widget.setItem(row, column, item)
            column += 1

    def get_selected_elements(self):
        elements = []
        for item in self.widget.selectedItems():
            if item.column() == 0:
                elements.append(int(item.text()))
        return elements

    def clear(self):
        self.widget.setRowCount(0)

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()


class AcqXanesParameters(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.register_persistents()
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
        self.ui.labelAcqXanesRoiWidth.hide()
        self.ui.spinBoxAcqXanesRoiWidth.hide()
        
    def connect_signals(self):
        self.ui.elementChooserAcqXanesElement.currentIndexChanged.connect( \
                self.update_element)
        self.ui.comboBoxAcqXanesEdge.currentIndexChanged.connect( \
                self.update_edge)

    def register_persistents(self):
        self.janus.utils["config"].add_persistent( \
                "acq_xanes", "transmission", self.ui.doubleSpinBoxAcqXanesTransmission.value,
                self.ui.doubleSpinBoxAcqXanesTransmission.setValue, float)
        self.janus.utils["config"].add_persistent( \
                "acq_xanes", "transmission_current", self.ui.checkBoxAcqXanesTransmission.isChecked,
                self.ui.checkBoxAcqXanesTransmission.setChecked, bool)
        self.janus.utils["config"].add_persistent( \
                "acq_xanes", "velocity", self.ui.doubleSpinBoxAcqXanesVelocity.value,
                self.ui.doubleSpinBoxAcqXanesVelocity.setValue, float)
        self.janus.utils["config"].add_persistent( \
                "acq_xanes", "energy_start", self.ui.spinBoxAcqXanesEnergyStart.value,
                self.ui.spinBoxAcqXanesEnergyStart.setValue, int)
        self.janus.utils["config"].add_persistent( \
                "acq_xanes", "energy_stop", self.ui.spinBoxAcqXanesEnergyStop.value,
                self.ui.spinBoxAcqXanesEnergyStop.setValue, int)
        self.janus.utils["config"].add_persistent( \
                "acq_xanes", "emission_energy", self.ui.spinBoxAcqXanesEmissionEnergy.value,
                self.ui.spinBoxAcqXanesEmissionEnergy.setValue, int)
        self.janus.utils["config"].add_persistent( \
                "acq_xanes", "emission_energy", self.ui.spinBoxAcqXanesEmissionEnergy.value,
                self.ui.spinBoxAcqXanesEmissionEnergy.setValue, int)
        self.janus.utils["config"].add_persistent( \
                "acq_xanes", "roi_width", self.ui.spinBoxAcqXanesRoiWidth.value,
                self.ui.spinBoxAcqXanesRoiWidth.setValue, int)

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


