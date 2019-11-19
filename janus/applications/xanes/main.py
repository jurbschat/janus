#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Apr 23, 2019

@author: janmeyer
'''

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from janus.core import Application
from janus.utils.log import Logger, LogHandler
from janus.utils.config import Config
from janus.widgets.log import Log
from janus.widgets.plot import Plot
from janus.widgets.acq_fluorescence import AcqXrfParameters, AcqXanesParameters, AcqRunParameters
from janus.devices.generic import Device
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, \
        QSizePolicy, QToolBox
from PyQt5.QtCore import Qt

class Xanes(Application):
    
    def __init__(self):
        Application.__init__(self, title="Xanes")

    def init_utils(self, pre=False, post=False):
        if pre:
            self.janus.utils["logger"] = Logger()
            self.janus.utils["logHandler"] = LogHandler()
            self.janus.utils["logger"].addHandler(self.janus.utils["logHandler"])
            self.janus.utils["config"] = Config("config.ini")
        if post:
            self.janus.utils["config"].load_persistent()

    def init_devices(self):
#         connector, path = self.janus.utils["config"].geturi("devices", "pressure1")
#         self.janus.devices["pressure1"] = Device(connector, path, \
#                 [{"name": "pressure", "attr": "Value", "mode": "read", "type": float, "delta": 0.001}])
        pass

    def init_widgets(self):
        self.janus.widgets["mainwindow"] = QMainWindow()
        self.janus.widgets["mainwindow"].setWindowTitle(self.applicationName())
        central_widget = QWidget(self.janus.widgets["mainwindow"])
        self.janus.widgets["mainwindowlayout"] = QHBoxLayout(central_widget)
        self.janus.widgets["mainwindow"].resize(1368, 768)
        self.janus.widgets["mainwindow"].setCentralWidget(central_widget)
        #plot
        self.janus.widgets["plot"] = Plot(central_widget)
#         self.janus.widgets["plot"].add_plot_data(0, data_type=Plot.TYPE_TIME, \
#                 role=Plot.ROLE_MASTER, interval=0.1, length=300)
#         self.janus.widgets["plot"].add_plot_data(1, data_type=Plot.TYPE_SCALAR, \
#                 attr=self.janus.devices["pressure1"].pressure, length=300)
#         self.janus.widgets["plot"].add_plot_data(2, data_type=Plot.TYPE_SCALAR, \
#                 attr=self.janus.devices["pressure2"].pressure, length=300)
#         self.janus.widgets["plot"].add_plot_item(0, 0, 1)
#         self.janus.widgets["plot"].add_plot_item(1, 0, 2, Qt.blue)
#         self.janus.widgets["plot"].tie_x_range(0)
        self.janus.widgets["plot"].widget.setSizePolicy(QSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.janus.widgets["mainwindowlayout"].addWidget(self.janus.widgets["plot"].widget, 3)
        #acquisition methods
        methods_row_widget = QWidget(central_widget)
        self.janus.widgets["methodrowlayout"] = QVBoxLayout(methods_row_widget)
        self.janus.widgets["acqmethods"] = QToolBox(central_widget)

        self.janus.widgets["acqxrf"] = AcqXrfParameters(self.janus.widgets["acqmethods"])
        self.janus.widgets["acqmethods"].addItem(self.janus.widgets["acqxrf"].widget, "XRF spectrum")
        self.janus.widgets["acqxanes"] = AcqXanesParameters(self.janus.widgets["acqmethods"])
        self.janus.widgets["acqmethods"].addItem(self.janus.widgets["acqxanes"].widget, "XANES scan")
        self.janus.widgets["acqrun"] = AcqRunParameters(central_widget)
        self.janus.widgets["methodrowlayout"].addWidget(self.janus.widgets["acqmethods"], 3)
        self.janus.widgets["methodrowlayout"].addWidget(self.janus.widgets["acqrun"].widget, 1)
        self.janus.widgets["mainwindowlayout"].addWidget(methods_row_widget, 1)
        
        #self.janus.widgets["log"] = Log(parent=self.janus.widgets["mainwindow"], handler=self.janus.utils["logHandler"])
        #self.janus.widgets["mainwindowlayout"].addWidget(self.janus.widgets["log"].widget)

    def on_exit(self):
        self.janus.utils["config"].save_persistent()
        Application.quit()

if __name__ == '__main__':
    app = Xanes()
    app.start()
