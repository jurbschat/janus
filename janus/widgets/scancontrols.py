from ..core import Object
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget
from janus.widgets.ui.scan_ui import Ui_Scan
from ..actions.gridscanaction import GridScanAction


class ScanControls(QObject, Object):

    def __init__(self, parent=None, grid_controller=None, grid_axis_controller=None, raw_tango_devices=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.grid_controller = grid_controller
        self.grid_axis_controller = grid_axis_controller
        self.raw_tango_devices = raw_tango_devices
        self.setup_ui()
        self.connect_signals()


    def start_scan(self):
        if "grid_scan" not in self.janus.actions or self.janus.actions["grid_scan"] is None:
            action = GridScanAction(self.grid_controller, self.grid_axis_controller, self.raw_tango_devices)
            action.progress_signal.connect(self.action_progress)
            action.done_signal.connect(self.action_done)
            self.janus.actions["grid_scan"] = action
            action.start()

    def action_progress(self, progress_data):
        print("progress: {}".format(progress_data["progress"]))

    def action_done(self):
        self.janus.actions["grid_scan"] = None

    def connect_signals(self):
        self.ui.startScan.clicked.connect(self.start_scan)

    def setup_ui(self):
        self.widget = QWidget(self.parent)
        self.ui = Ui_Scan()
        self.ui.setupUi(self.widget)