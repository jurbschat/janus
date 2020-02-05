import time
import asyncio
from ..core import Object
from ..controllers.axiscontroller import GridAxisNames
from ..utils.shutter import get_full_window_shutter_data
from ..widgets.actionprogressdialog import ProgressDialog
from ..utils.asynciohelper import ThreadedEventLoop
from collections import OrderedDict
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from enum import IntEnum
import threading
from datetime import datetime
import math

class ActionBase:
    pass;

class ScanDirection(IntEnum):
    LEFT_TO_RIGHT = -1
    RIGHT_TO_LEFT = 1

class ScanMode(IntEnum):
    LEFT_TO_RIGHT = 0
    RIGHT_TO_LEFT = 1
    SNAKE_START_LEFT = 2
    SNAKE_START_RIGHT = 3
    BOTTOM_LEFT_TO_RIGHT = 4
    BOTTOM_RIGHT_TO_LEFT = 5
    BOTTOM_SNAKE_START_LEFT = 6
    BOTTOM_SNAKE_START_RIGHT = 7

class GridScanAction(QObject, Object):

    progress_signal = pyqtSignal(object)
    done_signal = pyqtSignal()

    def __init__(self, grid_controller=None, grid_axis_controller=None, raw_tango_devices=None, params={}):
        QObject.__init__(self)
        Object.__init__(self)
        self.grid_controller = grid_controller
        self.grid_axis_controller = grid_axis_controller
        self.raw_tango_devices = raw_tango_devices
        self.shutter_data = self.build_shutter_data()
        self.progress_data = {
            "windowTitle": "Bäm Progress!",
            "progress": 0,
            "conditions": OrderedDict({
                "prepare": False,
                "important1": False,
                "important2": False,
                "cleanup": False
            }),
            "details": OrderedDict({
                "hello": "muh",
                "there": "blobb",
                "idiot": "gaga"
            })
        }
        self.default_parameters = {
            "hole_distance": 20,
            "start_pos": QPointF(0, 0),
            "grid_angle": 5,
            "hole_count": 13,
            "acceleration_pulses": 0,
            "direction": ScanDirection.LEFT_TO_RIGHT,
            "scan_frequency": 1,
        }
        self.scan_parameters = { **self.default_parameters, **params }
        self.scan_parameters = { **self.scan_parameters, **self.get_scan_params_for_grid() }
        self.should_stop = False
        self.scan_device = self.raw_tango_devices["linear_scan_device"]
        self.progress_dialog = ProgressDialog(self.progress_data, parent=self.janus.widgets["mainwindow"])
        self.progress_dialog.abort_signal.connect(self.stop_action)
        self.thread = threading.Thread(target=self.run, name="GridScan")
        
    def get_scan_params_for_grid(self):
        hole_distance = self.grid_controller.chip.hole_distance.x()
        grid_angle = self.grid_controller.angle * -180 / math.pi
        return {
            "hole_distance": hole_distance,
            "grid_angle": grid_angle
        }

    def start(self):
        self.thread.start()

    def doProgress(self):
        self.progress_signal.emit(self.progress_data)
        self.progress_dialog.update_data(self.progress_data)

    def doDone(self):
        self.done_signal.emit()
        self.finish_dialog()

    def build_shutter_data(self):
        return get_full_window_shutter_data(self.grid_controller)

    def stop_action(self):
        self.should_stop = True

    def finish_dialog(self):
        self.progress_dialog.destroy()
        self.progress_dialog = None

    def move_wait_xy(self, point):
        self.grid_axis_controller.set_position(GridAxisNames.AXIS_X, point.x())
        self.grid_axis_controller.set_position(GridAxisNames.AXIS_Y, point.y())
        self.wait_move_completed()

    def move_wait_axis(self, axis, pos):
        self.grid_axis_controller.set_position(axis, pos)
        self.wait_move_completed()

    def wait_move_completed(self):
        while not self.grid_axis_controller.all_moves_completed():
            time.sleep(0.1)

    def focus_runner(self):
        pass

    def start_linear_scan(self):
        self.scan_device.connector.proxy.command_inout("StartUserTask1", "SCAN")
        time.sleep(0.1)

    def wait_for_linear_scan(self):
        while self.scan_device.connector.proxy.read_attribute("UserTask1Running").value:
            time.sleep(0.1)

    def stop_linear_scan(self):
        self.scan_device.connector.proxy.command_inout("StopUserTask1")

    def set_initial_linear_scan_params(self):
        g = self.scan_device.connector.proxy.command_inout("WriteRead", "FREQ={}".format(self.scan_parameters["scan_frequency"]))
        h = self.scan_device.connector.proxy.command_inout("WriteRead", "PULSES={}".format(self.scan_parameters["acceleration_pulses"]))
        a = self.scan_device.connector.proxy.command_inout("WriteRead", "DIST={}".format(self.scan_parameters["hole_distance"]))
        d = self.scan_device.connector.proxy.command_inout("WriteRead", "ANGLE={}".format(self.scan_parameters["grid_angle"]))

    def setup_pilc(self):
        self.pilcProxy.Stop()
        self.pilcProxy.write_attribute("AccelerationCount", int(self.parameters["acclPulses"]))
        self.pilcProxy.write_attribute("Windows", int(self.parameters["numWindows"]))
        self.pilcProxy.write_attribute("HighCount", int(self.parameters["numColumnsPerWindow"]))
        self.pilcProxy.write_attribute("LowCount", int(self.parameters["numVerticalGaps"]))
        self.pilcProxy.write_attribute("Delay", 500)
        self.pilcProxy.Start()

    def stop_scan(self):
        self.should_stop = True
        #TODO: stop scan script, stop motors, restore motor values

    def run(self):
        try:
            lines = self.grid_controller.lines
            if len(lines) < 0:
                return
            self.stop_linear_scan()
            self.wait_for_linear_scan()
            beam_offset = self.grid_controller.beam_center_reference.get() + self.grid_controller.beam_offset.get()
            self.set_initial_linear_scan_params()
            for idx, line in enumerate(lines):
                if self.should_stop:
                    break
                line_start = QPointF(-line["startPos"][0], -line["startPos"][1]) + beam_offset
                line_end = QPointF(-line["endPos"][0], -line["endPos"][1]) + beam_offset
                print("scanning line: {}".format(idx))
                start_pos = line_start if idx % 2 == 0 else line_end
                move_direction = int(self.scan_parameters["direction"]) * (1 if idx % 2 == 0 else -1)
                self.scan_device.connector.proxy.command_inout("WriteRead", "STARTX={}".format(start_pos.x()))
                self.scan_device.connector.proxy.command_inout("WriteRead", "STARTY={}".format(start_pos.y()))
                self.scan_device.connector.proxy.command_inout("WriteRead", "DIR={}".format(move_direction))
                self.scan_device.connector.proxy.command_inout("WriteRead", "NUM={}".format(line["hole_count"]))
                self.start_linear_scan()
                self.wait_for_linear_scan()
                if self.should_stop:
                    break
                self.progress_data["progress"] = (idx + 1) / len(lines)
                self.doProgress()
                time.sleep(0.1)
        except Exception as e:
            print(e)
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Scan aborted, error: {}".format(e))
            msg.setWindowTitle("Scan Aborted")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.show()
        self.doDone()




















