from ..core import Object
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from janus.widgets.ui.gridcontrols_ui import Ui_GridControls
import glm

class GridControls(QObject, Object):

    def __init__(self, parent=None, grid_controller=None, chip_registry=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.grid_controller = grid_controller
        self.chip_registry = chip_registry
        self.modified_chips = set()
        self.setup_ui()
        self.setup_info()
        self.connect_signals()

    def setup_info(self):
        self.config = self.janus.utils["config"]
        chip_list = self.chip_registry.get_chip_list()
        self.ui.chipSelection.clear()
        for idx, name in enumerate(chip_list):
            self.ui.chipSelection.addItem(name)
            self.ui.chipSelection.setItemData(idx, name, Qt.ToolTipRole)
        self.ui.chipSelection.setCurrentText(self.janus.utils["config"].get("grid", "selected_chip"))
        self.grid_controller.selected_chip_name.set(self.ui.chipSelection.currentText())
        self.janus.utils["config"].add_persistent("grid", "selected_chip", self.ui.chipSelection.currentText,
            self.ui.chipSelection.setCurrentText, str)

    def connect_signals(self):
        self.ui.beamSize.valueChanged.connect(self.beam_size_ui_changed)
        self.ui.beamOffsetX.valueChanged.connect(lambda value: self.beam_offset_ui_changed())
        self.ui.beamOffsetY.valueChanged.connect(lambda value: self.beam_offset_ui_changed())
        self.ui.chipSelection.currentTextChanged.connect(self.chip_selection_changed)
        self.ui.chipOriginX.valueChanged.connect(lambda value: self.chip_origin_changed())
        self.ui.chipOriginY.valueChanged.connect(lambda value: self.chip_origin_changed())
        self.ui.saveUpdatedChipData.clicked.connect(lambda: self.save_chip_data())
        self.ui.fullWindowsOnly.clicked.connect(lambda checked: self.draw_original_changed(checked))

        self.grid_controller.beam_size.register(self.beam_size_external_change)
        self.grid_controller.beam_offset.register(self.beam_offset_external_change)

    def draw_original_changed(self, checked):
        self.grid_controller.generate_only_full_windows.set(checked)

    def chip_selection_changed(self, chip_name):
        if self.grid_controller.selected_chip_name.get() == chip_name:
            return
        self.grid_controller.selected_chip_name.set(chip_name)
        if chip_name in self.modified_chips:
            self.ui.chipOriginX.setStyleSheet("background-color: yellow")
            self.ui.chipOriginY.setStyleSheet("background-color: yellow")
        else:
            self.ui.chipOriginX.setStyleSheet("background-color: white")
            self.ui.chipOriginY.setStyleSheet("background-color: white")
        self.ui.chipOriginX.blockSignals(True)
        self.ui.chipOriginY.blockSignals(True)
        chip = self.chip_registry.get_chip(chip_name)
        self.ui.chipOriginX.setValue(chip.origin_offset.x())
        self.ui.chipOriginY.setValue(chip.origin_offset.y())
        self.ui.chipOriginX.blockSignals(False)
        self.ui.chipOriginY.blockSignals(False)

    def beam_size_ui_changed(self, value):
        self.grid_controller.beam_size.unregister(self.beam_size_external_change)
        self.grid_controller.beam_size.set(value)
        self.grid_controller.beam_size.register(self.beam_size_external_change)

    def beam_size_external_change(self, value):
        self.ui.beamSize.blockSignals(True)
        self.ui.beamSize.setValue(value)
        self.ui.beamSize.blockSignals(False)

    def beam_offset_ui_changed(self):
        self.grid_controller.beam_offset.unregister(self.beam_offset_external_change)
        self.grid_controller.beam_offset.set(QPointF(self.ui.beamOffsetX.value(), self.ui.beamOffsetY.value()))
        self.grid_controller.beam_offset.register(self.beam_offset_external_change)

    def beam_offset_external_change(self, value):
        self.ui.beamOffsetX.blockSignals(True)
        self.ui.beamOffsetY.blockSignals(True)
        self.ui.beamOffsetX.setValue(value.x())
        self.ui.beamOffsetY.setValue(value.y())
        self.ui.beamOffsetX.blockSignals(False)
        self.ui.beamOffsetY.blockSignals(False)

    def chip_origin_changed(self):
        chip = self.chip_registry.get_chip(self.grid_controller.selected_chip_name.get())
        chip.origin_offset = QPointF(self.ui.chipOriginX.value(), self.ui.chipOriginY.value())
        self.ui.chipOriginX.setStyleSheet("background-color: yellow")
        self.ui.chipOriginY.setStyleSheet("background-color: yellow")
        self.modified_chips.add(chip.name)
        self.chip_registry.update_chip(chip)

    def save_chip_data(self):
        self.config.save_persistent()
        self.modified_chips = set()
        self.ui.chipOriginX.setStyleSheet("background-color: white")
        self.ui.chipOriginY.setStyleSheet("background-color: white")

    def setup_ui(self):
        self.widget = QWidget(self.parent)
        self.ui = Ui_GridControls()
        self.ui.setupUi(self.widget)

    def save(self):
        pass
