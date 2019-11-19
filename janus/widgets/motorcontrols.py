from ..core import Object
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget
from janus.widgets.ui.motorcontrols_ui import Ui_MotorControls

class MotorControls(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.connect_signals()

    def connect_signals(self):
        self.ui.doubleSpinBox.valueChanged.connect(self.myfct)

    def myfct(self, value):
        print(value)

    def setup_ui(self):
        self.widget = QWidget(self.parent)
        self.ui = Ui_MotorControls()
        self.ui.setupUi(self.widget)

    def save(self):
        pass