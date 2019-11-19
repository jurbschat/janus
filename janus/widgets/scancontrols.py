from ..core import Object
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget
from janus.widgets.ui.scan_ui import Ui_Scan

class ScanControls(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.connect_signals()

    def connect_signals(self):
        pass

    def setup_ui(self):
        self.widget = QWidget(self.parent)
        self.ui = Ui_Scan()
        self.ui.setupUi(self.widget)

    def save(self):
        pass