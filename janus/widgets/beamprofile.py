from ..core import Object
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget
from janus.widgets.ui.beamprofile_ui import Ui_BeamProfile
from janus.utils.eventhub import global_event_hub, Event as EHEvent, EventType as EHEventType


class BeamProfile(QObject, Object):

    def __init__(self, parent=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.setup_ui()
        self.connect_signals()

    def connect_signals(self):
        self.ui.alignCenterButton.clicked.connect(self.align_clicked)
        pass

    def align_clicked(self):
        global_event_hub().send(EHEvent(EHEventType.ALIGN_BEAMOFFSET_TO_BEAMPROFILE))

    def setup_ui(self):
        self.widget = QWidget(self.parent)
        self.ui = Ui_BeamProfile()
        self.ui.setupUi(self.widget)

    def save(self):
        pass