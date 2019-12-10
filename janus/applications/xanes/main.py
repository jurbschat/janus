#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-BMX, FS-Petra-D, P11"
__license__ = "GPL"


import os
import sys
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, \
        QSizePolicy, QToolBox
from PyQt5.QtCore import Qt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from janus.core import Application
from janus.utils.log import Logger, LogHandler, StdoutHandler
from janus.utils.config import Config
from janus.widgets.log import Log
from janus.widgets.plot import Plot
from janus.widgets.acq import AcqRunParameters, AcqProgressDialog
from janus.widgets.acq_fluorescence import AcqXrfParameters, AcqXanesParameters
from janus.devices.fluorescence import Xspress3
from janus.devices.generic import Device
from janus.devices.p11 import P11Shutter, P11Filters
from janus.actions.acq import AcqHandler
from janus.actions.acq_fluorescence import AcqXrfSpectrum, AcqXanesScan

class Xanes(Application):
    
    def __init__(self):
        Application.__init__(self, title="Xanes")

    def init_utils(self, pre=False, post=False):
        if pre:
            self.janus.utils["logger"] = Logger()
            #self.janus.utils["loghandler"] = LogHandler()
            self.janus.utils["logger"].addHandler(StdoutHandler())
            self.janus.utils["config"] = Config("config.ini")
        if post:
            self.janus.utils["config"].load_persistent()

    def init_devices(self):
        connector, path = self.janus.utils["config"].geturi("devices", "shutter0")
        self.janus.devices["bs0"] = P11Shutter(connector, path)
        connector, path = self.janus.utils["config"].geturi("devices", "shutter1")
        self.janus.devices["bs1"] = P11Shutter(connector, path)
        connector, path = self.janus.utils["config"].geturi("devices", "fastshutter")
        self.janus.devices["fs"] = P11Shutter(connector, path)
        connector, path = self.janus.utils["config"].geturi("devices", "interlock")
        self.janus.devices["interlock"] = Device(connector, path,
                [{"name": "value", "attr": "Value", "mode": "read", "type": bool}])
        if connector == "simulation":
            self.janus.devices["interlock"].connector.write("value", True)
        connector, path = self.janus.utils["config"].geturi("devices", "energy")
        self.janus.devices["energy"] = Device(connector, path,
                [{"name": "energy", "attr": "Energy", "mode": "write", "type": float},
                {"name": "auto_brake", "attr": "AutoBrake", "mode": "write", "type": bool},
                {"name": "brake", "attr": "Brake", "mode": "execute"},
                {"name": "move", "attr": "Move", "mode": "execute"}])
        connector, path = self.janus.utils["config"].geturi("devices", "filter")
        self.janus.devices["filter"] = P11Filters(connector, path)
        connector, path = self.janus.utils["config"].geturi("devices", "xspress3")
        self.janus.devices["xspress3"] = Xspress3(connector, path)

    def init_widgets(self):
        self.janus.widgets["mainwindow"] = QMainWindow()
        self.janus.widgets["mainwindow"].setWindowTitle(self.applicationName())
        central_widget = QWidget(self.janus.widgets["mainwindow"])
        self.janus.widgets["mainwindowlayout"] = QHBoxLayout(central_widget)
        self.janus.widgets["mainwindow"].resize(1368, 768)
        self.janus.widgets["mainwindow"].setCentralWidget(central_widget)
        #plot
        self.janus.widgets["plot"] = Plot(central_widget)
        self.janus.widgets["plot"].add_plot_data(0, data_type=Plot.TYPE_STATIC,
                data=self.janus.devices["xspress3"].bin_energies())
        self.janus.widgets["plot"].add_plot_data(1, data_type=Plot.TYPE_SPECTRUM,
                attr=self.janus.devices["xspress3"].channel1)
#         self.janus.widgets["plot"].add_plot_data(2, data_type=Plot.TYPE_SCALAR, \
#                 attr=self.janus.devices["pressure2"].pressure, length=300)
        self.janus.widgets["plot"].add_plot_item(0, 0, 1)
#         self.janus.widgets["plot"].add_plot_item(1, 0, 2, Qt.blue)
        self.janus.widgets["plot"].tie_x_range(0)
        self.janus.widgets["plot"].widget.setSizePolicy(QSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding))
        self.janus.widgets["plot"].widget.setLabels(left="events", bottom="eV")
        self.janus.widgets["mainwindowlayout"].addWidget(self.janus.widgets["plot"].widget, 3)
        #acquisition methods
        methods_row_widget = QWidget(central_widget)
        self.janus.widgets["methodrowlayout"] = QVBoxLayout(methods_row_widget)
        self.janus.widgets["acqmethods"] = QToolBox(central_widget)
        self.janus.widgets["acqxrf"] = AcqXrfParameters(self.janus.widgets["acqmethods"])
        self.janus.widgets["acqmethods"].addItem(self.janus.widgets["acqxrf"].widget, "XRF Spectrum")
        self.janus.widgets["acqxanes"] = AcqXanesParameters(self.janus.widgets["acqmethods"])
        self.janus.widgets["acqmethods"].addItem(self.janus.widgets["acqxanes"].widget, "XANES Scan")
        self.janus.widgets["acqrun"] = AcqRunParameters(central_widget)
        self.janus.widgets["methodrowlayout"].addWidget(self.janus.widgets["acqmethods"], 3)
        self.janus.widgets["methodrowlayout"].addWidget(self.janus.widgets["acqrun"].widget, 1)
        self.janus.widgets["mainwindowlayout"].addWidget(methods_row_widget, 1)
        self.janus.widgets["acqprogressdialog"] = AcqProgressDialog(self.janus.widgets["mainwindow"])

        #self.janus.widgets["log"] = Log(parent=self.janus.widgets["mainwindow"], handler=self.janus.utils["logHandler"])
        #self.janus.widgets["mainwindowlayout"].addWidget(self.janus.widgets["log"].widget)

    def init_actions(self):
        self.janus.actions["acqxrf"] = AcqXrfSpectrum()
        self.janus.actions["acqxanes"] = AcqXanesScan()
        self.janus.actions["acqhandler"] = AcqHandler(
                self.janus.widgets["acqmethods"], 
                self.janus.widgets["acqrun"].ui.pushButtonStartAcq)
        self.janus.actions["acqhandler"].associate(
                self.janus.widgets["acqxrf"].widget,
                self.janus.actions["acqxrf"])
        self.janus.actions["acqhandler"].associate(
                self.janus.widgets["acqxanes"].widget,
                self.janus.actions["acqxanes"])

    def on_exit(self):
        self.janus.utils["config"].save_persistent()
        Application.quit()

if __name__ == '__main__':
    app = Xanes()
    app.start()
