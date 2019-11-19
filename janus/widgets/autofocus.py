from ..core import Object
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget
from ui.autofocus_ui import Ui_Autofocus

class Autofocus(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.validInputs = {}
        self.log = self.janus.utils["logger"]
        self.afc = self.janus.devices["autofocus"]
        self.focusRunning = False
        self.connect_signals()

    def connect_signals(self):
        self.ui.quantSlider.valueChanged.connect(self.quantSliderChanged)
        self.ui.delaySlider.valueChanged.connect(self.delaySliderChanged)
        self.ui.goalSlider.valueChanged.connect(self.goalSliderChanged)
        self.ui.quantEdit.textChanged.connect(self.quantEditChanged)
        self.ui.delayEdit.textChanged.connect(self.delayEditChanged)
        self.ui.goalEdit.textChanged.connect(self.goalEditChanged)
        self.ui.startFocus.clicked.connect(self.startClicked)
        self.afc.focus_done.connect(self.focusDone)


    def is_number(self, str):
        try:
            float(str)
            return True
        except ValueError:
            return False

    def is_int(self, str):
        try:
            int(str)
            return True
        except ValueError:
            return False

    def quantSliderChanged(self, value):
        self.log.info("quant!")
        editText = "{0:.2f}".format(value / self.ui.quantSlider.maximum()).rstrip('0').rstrip('.')
        self.ui.quantEdit.setText(editText)
        pass

    def goalSliderChanged(self, value):
        self.log.info("goal!")
        editText = "{0:.2f}".format(value / self.ui.quantSlider.maximum()).rstrip('0').rstrip('.')
        self.ui.goalEdit.setText(editText)
        pass

    def delaySliderChanged(self, value):
        self.log.info("delay!")
        editText = str(value)
        self.ui.delayEdit.setText(editText)
        pass

    def quantEditChanged(self, value):
        if not self.process_and_validate_edit_input(value, "quant", self.is_number):
            return;
        value = int(float(value) * self.ui.quantSlider.maximum());
        self.ui.quantSlider.setValue(value)

    def goalEditChanged(self, value):
        if not self.process_and_validate_edit_input(value, "goal", self.is_number):
            return;
        value = int(float(value) *  self.ui.quantSlider.maximum());
        self.ui.goalSlider.setValue(value)

    def delayEditChanged(self, value):
        if not self.process_and_validate_edit_input(value, "delay", self.is_int):
            return;
        value = int(value);
        self.ui.delaySlider.setValue(value)

    def process_and_validate_edit_input(self, value, name, validateFct):
        if not validateFct(value):
            self.validInputs[name] = False;
            self.set_start_focus_btn_state()
            return False
        self.validInputs[name] = True;
        self.set_start_focus_btn_state()
        return True

    def set_start_focus_btn_state(self):
        if self.focusRunning:
            return False
        for key in self.validInputs:
            val = self.validInputs[key]
            if not val:
                self.ui.startFocus.setEnabled(False)
                return
        self.ui.startFocus.setEnabled(True)

    def startClicked(self):
        self.focusRunning = True
        self.set_start_focus_btn_state()
        quant = self.ui.quantSlider.value() / self.ui.quantSlider.maximum()
        goal = self.ui.goalSlider.value() / self.ui.goalSlider.maximum()
        delay = self.ui.delaySlider.value()
        self.afc.start_autofocus(quant, goal, delay)

    def focusDone(self):
        self.focusRunning = False
        self.set_start_focus_btn_state()

    def setup_ui(self):
        self.widget = QWidget(self.parent)
        self.ui = Ui_Autofocus()
        self.ui.setupUi(self.widget)

    def save(self):
        pass