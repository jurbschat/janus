from ..core import Object
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

class MainMenuBar(QObject, Object):

    def __init__(self, mainWindow):
        QObject.__init__(self)
        Object.__init__(self)
        self.menuBar = mainWindow.menuBar()
        self.fileMenu = self.menuBar.addMenu('&File')

        extractAction = QAction("&GET TO THE CHOPPAH!!!", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Leave The App')
        extractAction.triggered.connect(self.close_application)

        self.add_action(self.fileMenu, extractAction)

    def close_application(self):
        print("whooaaaa so custom!!!")
        sys.exit()

    def find_menu(self, path):
        if path is None or len(path) == 0:
            return None
        self.menuBar.actions()
        isLast = len(path) == 1
        for actionOrMenu in self.menuBar.actions():
            if actionOrMenu.menu():
                if actionOrMenu.text() == path[0]:
                    if isLast:
                        return actionOrMenu
                    else:
                        return self.find_menu(path[1:])
        return None

    def add_menu(self, parent, menu):
        parent.addAction(menu)

    def add_action(self, menu, action):
        menu.addAction(action)