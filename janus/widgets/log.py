'''
Created on May 29, 2019

@author: janmeyer
'''

from ..core import Object
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import QWidget


class Log(QObject, Object):
    
    def __init__(self, parent=None, handler=None):
        Object.__init__(self)
        QObject.__init__(self)
        self.parent = parent
        self.handler = handler
        self.setup_ui()
        self._set_view_level(0)
        self.ui.textEditLog.setText(self.handler.text)
        self.register_persistents()
        self.connect_signals()

    def connect_signals(self):
        self.ui.comboBoxLogLevel.currentIndexChanged.connect(self._set_view_level)
        self.ui.pushButtonLogSave.clicked.connect(self.save)
        self.handler.value_changed.connect(self.update_values)

    def register_persistents(self):
        self.janus.utils["config"].add_persistent( \
                "log", "view_level", self.ui.comboBoxLogLevel.currentIndex,
                self.ui.comboBoxLogLevel.setCurrentIndex, int)

    def update_values(self, msg):
        if msg is None:
            self.ui.textEditLog.setText(self.handler.text)
        else:
            self.ui.textEditLog.append(msg)

    def _set_view_level(self, dummy):
        level = (self.ui.comboBoxLogLevel.currentIndex() + 1) * 10
        self.handler.set_view_level(level)

    def setup_ui(self):
        from .ui.log_ui import Ui_QWidgetLog
        self.widget = QWidget(self.parent)
        self.ui = Ui_QWidgetLog()
        self.ui.setupUi(self.widget)

    def save(self):
        pass