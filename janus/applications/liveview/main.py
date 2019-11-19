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
from janus.devices.camera import VimbaCamera
from janus.controllers.gridcontroller import GridController, AABBPointGenerator, ChipPointGenerator
from janus.controllers.axiscontroller import AxisController
from janus.controllers.chipregistry import ChipRegistry
#from janus.devices.autofocuscontroller import AutofocusController
from janus.devices.motor import TangoMotor
from janus.widgets.camera import CameraControls
from janus.widgets.gridwidget import GridWidget, GridAxisNames
from janus.widgets.log import Log
from janus.widgets.gridcontrols import GridControls
from janus.widgets.beamprofile import BeamProfile
from janus.widgets.motorcontrols import MotorControls
from janus.widgets.scancontrols import ScanControls
from janus.widgets.statusbar import StatusBar
from janus.widgets.mainmenubar import MainMenuBar
from janus.widgets.gridtoolbar import GridToolBar
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import glm

class RememberedMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent)
        self.readSettings()

    def closeEvent(self, event):
        print('closing, goodbye :)')
        settings = QSettings("desy", "janus")
        settings.setValue('geometry', self.saveGeometry())
        settings.setValue('windowState', self.saveState())
        super(QMainWindow, self).closeEvent(event)

    def readSettings(self):
        settings = QSettings("desy", "janus")
        geom = settings.value("geometry")
        state = settings.value("windowState")
        if geom is not None:
            self.restoreGeometry(geom)
        if state is not None:
            self.restoreState(state)


class LiveView(Application):
    
    def __init__(self):
        Application.__init__(self, title="LiveView")
        if os.name == 'nt':
            self.setStyle("Fusion")

    def init_utils(self, pre=False, post=False):
        if pre:
            self.janus.utils["logger"] = Logger()
            self.janus.utils["logHandler"] = LogHandler()
            self.janus.utils["logger"].addHandler(self.janus.utils["logHandler"])
            self.janus.utils["config"] = Config("config.ini")
        if post:
            self.janus.utils["config"].load_persistent()

    def init_devices(self):
        connector, onaxis_camera = self.janus.utils["config"].geturi("devices", "onaxis_camera")
        vimba_on_axis = VimbaCamera(connector, onaxis_camera)
        vimba_on_axis.exposure_time_max(200000)
        self.janus.devices["onaxis_camera"] = vimba_on_axis

        con_motor_rr_linear, motor_rr_linear = self.janus.utils["config"].geturi("devices", "motor_rr_linear")
        #con_motor_rr_rotation, motor_rr_rotation = self.janus.utils["config"].geturi("devices", "motor_rr_rotation")
        #con_motor_rr_centerx, motor_rr_centerx = self.janus.utils["config"].geturi("devices", "motor_rr_center_x")
        #con_motor_rr_centery, motor_rr_centery = self.janus.utils["config"].geturi("devices", "motor_rr_center_y")
        #con_motor_tower_x, motor_tower_x = self.janus.utils["config"].geturi("devices", "motor_tower_x")
        con_motor_tower_y, motor_tower_y = self.janus.utils["config"].geturi("devices", "motor_tower_y")
        con_motor_tower_z, motor_tower_z = self.janus.utils["config"].geturi("devices", "motor_tower_z")

        self.janus.devices["motor_rr_linear"] = TangoMotor(connector=con_motor_rr_linear, uri=motor_rr_linear, updateInterval=0.020)
        #self.janus.devices["motor_rr_rotation"] = TangoMotor(connector=con_motor_rr_rotation, uri=motor_rr_rotation, updateInterval=0.020)
        #self.janus.devices["motor_rr_centerx"] = TangoMotor(connector=con_motor_rr_centerx, uri=motor_rr_centerx, updateInterval=0.020)
        #self.janus.devices["motor_rr_centery"] = TangoMotor(connector=con_motor_rr_centery, uri=motor_rr_centery, updateInterval=0.020)
        #self.janus.devices["motor_tower_x"] = TangoMotor(connector=con_motor_tower_x, uri=motor_tower_x, updateInterval=0.020)
        self.janus.devices["motor_tower_y"] = TangoMotor(connector=con_motor_tower_y, uri=motor_tower_y, updateInterval=0.020)
        self.janus.devices["motor_tower_z"] = TangoMotor(connector=con_motor_tower_z, uri=motor_tower_z, updateInterval=0.020)

    def init_controllers(self):
        chip_registry = ChipRegistry("chips.xml")
        self.janus.controllers["chip_registry"] = chip_registry
        #_, focusaxis = self.janus.utils["config"].geturi("devices", "motor_tower_z")
        #self.janus.controllers["autofocus"] = AutofocusController(camera, focusaxis)
        devices = {
            GridAxisNames.AXIS_X: self.janus.devices["motor_rr_linear"],
            GridAxisNames.AXIS_Y: self.janus.devices["motor_tower_y"],
            GridAxisNames.AXIS_Z: self.janus.devices["motor_tower_z"]
        }
        self.janus.controllers["grid_axis_controller"] = AxisController(devices)
        chip = chip_registry.get_chip("new-format")
        self.janus.controllers["grid"] = GridController(ChipPointGenerator([glm.vec2(0, 0), 
                glm.vec2(chip.chip_size.x, 0), 
                glm.vec2(chip.chip_size.x, chip.chip_size.y), 
                glm.vec2(0, chip.chip_size.y)
            ], 
            chip))
        #self.janus.controllers["grid"] = GridController()

    def init_widgets(self):
        mainWindow = RememberedMainWindow()
        self.janus.widgets["mainwindow"] = mainWindow
        mainWindow.setWindowTitle(self.applicationName())
        central_widget = QWidget(mainWindow)
        mainLayout = QVBoxLayout(central_widget)
        mainWindow.setCentralWidget(central_widget)
        self.janus.widgets["mainWindowlayout"] = mainLayout

        #
        # setup main splitter
        #
        splitter = QSplitter(central_widget)

        #
        # layout and widget for the controls on the right
        #
        controlsScrollArea = QScrollArea(splitter)
        controlsScrollArea.setWidgetResizable(True)

        scrollAreaWidget = QWidget()
        scrollAreaLAyout = QVBoxLayout(scrollAreaWidget)

        cameraControls = CameraControls(parent=scrollAreaWidget, device=self.janus.devices["onaxis_camera"])
        self.janus.widgets["cameraControls"] = cameraControls
        scrollAreaLAyout.addWidget(cameraControls.widget)

        # grid controls
        gridControls = GridControls(parent=scrollAreaWidget, grid_controller=self.janus.controllers["grid"], chip_registry=self.janus.controllers["chip_registry"])
        self.janus.widgets["gridControls"] = gridControls
        scrollAreaLAyout.addWidget(gridControls.widget)

        # scan controls
        scanControls = ScanControls(parent=scrollAreaWidget)
        self.janus.widgets["scanControls"] = scanControls
        scrollAreaLAyout.addWidget(scanControls.widget)

        # motorcontrols controls
        motorControls = MotorControls(parent=scrollAreaWidget)
        self.janus.widgets["motorControls"] = motorControls
        scrollAreaLAyout.addWidget(motorControls.widget)

        beamProfile = BeamProfile(parent=scrollAreaWidget)
        self.janus.widgets["beamProfile"] = beamProfile
        scrollAreaLAyout.addWidget(beamProfile.widget)

        # log console
        logView = Log(parent=scrollAreaWidget, handler=self.janus.utils["logHandler"])
        self.janus.widgets["logView"] = logView
        scrollAreaLAyout.addWidget(logView.widget)

        # all the bars!
        #self.janus.widgets["menuBar"] = MainMenuBar(mainWindow)
        self.janus.widgets["statusBar"] = StatusBar(mainWindow)

        controlsScrollArea.setWidget(scrollAreaWidget)

        #
        # left side camera stuff
        #
        cameraSceneWidget = QWidget(splitter)
        cameraSceneLayout = QVBoxLayout(cameraSceneWidget)
        cameraSceneLayout.setContentsMargins(6, 0, 6, 0)

        onaxis = self.janus.devices["onaxis_camera"]
        axis_controller = self.janus.controllers["grid_axis_controller"]
        grid = self.janus.controllers["grid"]
        chip_registry = self.janus.controllers["chip_registry"]
        grid_widget = GridWidget(parent=cameraSceneWidget, grid_controller=grid, camera=onaxis, axis_controller=axis_controller, chip_registry=chip_registry)
        self.janus.widgets["gridWidget"] = grid_widget

        gridToolbar = GridToolBar(cameraSceneWidget, grid_widget)
        self.janus.widgets["toolBar"] = gridToolbar

        cameraSceneLayout.addWidget(gridToolbar.widget)
        cameraSceneLayout.addWidget(grid_widget)
        cameraSceneWidget.setLayout(cameraSceneLayout)

        splitter.addWidget(cameraSceneWidget)
        splitter.addWidget(controlsScrollArea)
        splitter.setCollapsible(0, False)
        splitter.setCollapsible(1, False)
        splitter.setStretchFactor(0, 250)
        splitter.setStretchFactor(1, 100)

        mainLayout.addWidget(splitter)

    def on_exit(self):
        for dev in self.janus.controllers:
            self.janus.controllers[dev].stop_controller()
        for dev in self.janus.devices:
            self.janus.devices[dev].stop_device()
        self.janus.utils["config"].save_persistent()
        Application.quit()

if __name__ == '__main__':
    app = LiveView()
    app.start()
