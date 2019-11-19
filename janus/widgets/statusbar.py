from ..core import Object
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class StatusBar(QObject, Object):

    def __init__(self, mainWindow):
        QObject.__init__(self)
        Object.__init__(self)
        self.statusBar = mainWindow.statusBar()
        mainWindow.statusBar().showMessage('Message in statusbar.')

    def get_status_bar(self):
        return self.statusBar