'''
Created on Apr 8, 2019

@author: janmeyer
'''

import os
import sys
import signal
from PyQt5.QtWidgets import QApplication, QSplashScreen, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QDir

class Object(object):

    def __init__(self):
        self.janus = sys.modules["__main__"]

class Application(QApplication, Object):

    def __init__(self, title="Janus", splash=None):
        Object.__init__(self)
        QApplication.__init__(self, sys.argv)
        self.setApplicationName(title)
        self.janus.application = self
        self.path = os.path.realpath(os.path.dirname(sys.argv[0]))
        QDir.addSearchPath("icons", \
                os.path.realpath(os.path.dirname(__file__)) + "/widgets/icons")
        self.splash = None
        if splash is not None:
            if os.access(self.path + splash, os.R_OK):
                self.splash = QPixmap(self.path + splash)
        self.janus.utils = dict()
        self.janus.devices = dict()
        self.janus.widgets = dict()
        self.janus.actions = dict()
        self.janus.controllers = dict()
        self.aboutToQuit.connect(self.on_exit)
    
    def start(self):
        #register signal handler
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        #show splash screen
        splash = None
        if self.splash is not None:
            splash = QSplashScreen(self.splash)
            splash.setMask(self.splash.mask())
            splash.show()
        #init modules
        if self.splash is not None:
            splash.showMessage("\n\n   Importing utils...")
        self.init_utils(pre=True)
        if self.splash is not None:
            splash.showMessage("\n\n   Importing devices...")
        self.init_devices()
        if self.splash is not None:
            splash.showMessage("\n\n   Importing controllers...")
        self.init_controllers()
        if self.splash is not None:
            splash.showMessage("\n\n   Importing widgets...")
        self.init_widgets()
        if self.splash is not None:
            splash.showMessage("\n\n   Importing actions...")
        self.init_actions()
        if self.splash is not None:
            splash.showMessage("\n\n   Importing utils...")
        self.init_utils(post=True)
        if self.splash is not None:
            splash.showMessage("\n\n   finished...")
            splash.finish(self.janus.widgets["mainwindow"])
        #start application
        self.processEvents()
        self.janus.widgets["mainwindow"].show()
        retCode = self.exec_()
        sys.exit(retCode)

    def init_utils(self, pre=False, post=False):
        pass

    def init_devices(self):
        pass

    def init_controllers(self):
        pass

    def init_widgets(self):
        self.janus.widgets["mainwindow"] = QMainWindow()
        self.janus.widgets["mainwindow"].setWindowTitle(self.applicationName())

    def init_actions(self):
        pass

    def on_exit(self):
        pass
