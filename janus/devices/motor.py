"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-BMX, FS-Petra-D, P11"
__license__ = "GPL"


from PyQt5.QtCore import QObject, pyqtSignal
from PyTango import DeviceProxy
from ..core import Object
from ..const import UpdatePolicy, State
from .connector import SimulationConnector, TangoConnector
from .devicebase import DeviceBase


class Motor(Object, QObject, DeviceBase):

    value_changed = pyqtSignal(str, name="valueChanged")

    def __init__(self):
        QObject.__init__(self)
        Object.__init__(self)
        self.attributes = { \
            "state": {"mode": "read", "type": State},
            "position": {"mode": "write", "type": float},
            "velocity": {"mode": "write", "type": float},
            "acceleration": {"mode": "write", "type": float},
            "soft_limit_min": {"mode": "write", "type": float},
            "soft_limit_max": {"mode": "write", "type": float},
            "soft_limit_min_fault": {"mode": "read", "type": bool},
            "soft_limit_max_fault": {"mode": "read", "type": bool},
            "hard_limit_min_fault": {"mode": "read", "type": bool},
            "hard_limit_max_fault": {"mode": "read", "type": bool},
            "stop": {"mode": "exec"},
            "calibrate": {"mode": "exec"},
        }

    def state(self, refresh=False):
        return self.connector.state(refresh)

    def position(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("position", float(value))
        else:
            return self.connector.read("position", refresh, alt)

    def velocity(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("velocity", float(value))
        else:
            return self.connector.read("velocity", refresh, alt)

    def acceleration(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("acceleration", float(value))
        else:
            return self.connector.read("acceleration", refresh, alt)

    def soft_limit_min(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("soft_limit_min", float(value))
        else:
            return self.connector.read("soft_limit_min", refresh, alt)

    def soft_limit_max(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("soft_limit_max", float(value))
        else:
            return self.connector.read("soft_limit_max", refresh, alt)

    def soft_limit_min_fault(self, refresh=False, alt=None):
        return self.connector.read("soft_limit_min_fault", refresh, alt)

    def soft_limit_max_fault(self, refresh=False, alt=None):
        return self.connector.read("soft_limit_max_fault", refresh, alt)

    def hard_limit_min_fault(self, refresh=False, alt=None):
        return self.connector.read("hard_limit_min_fault", refresh, alt)

    def hard_limit_max_fault(self, refresh=False, alt=None):
        return self.connector.read("hard_limit_max_fault", refresh, alt)

    def stop(self):
        self.connector.execute("stop")

    def calibrate(self, value=None):
        if value is not None:
            self.connector.execute("calibrate", value)


class TangoMotor(Motor):
    
    value_changed = pyqtSignal(str, name="valueChanged")

    def __init__(self, connector=None, uri=None, updateInterval = 0.02):
        Motor.__init__(self)
        self.uri = uri
        self.type = "Simulation"
        attributes = {}
        attributes["AerotechEnsemble"] = [ \
                {"attr": "Position", "delta": 0.1},
                {"attr": "Velocity"},
                {"attr": "Acceleration"},
                {"attr": "SoftLimitCcw", "name": "soft_limit_min"},
                {"attr": "SoftLimitCw", "name": "soft_limit_max"},
                {"attr": "CcwSoftLimitFault", "name": "soft_limit_min_fault"},
                {"attr": "CwSoftLimitFault", "name": "soft_limit_max_fault"},
                {"attr": "CcwLimitFault", "name": "hard_limit_min_fault"},
                {"attr": "CwLimitFault", "name": "hard_limit_max_fault"},
                {"attr": "AbortMove", "name": "stop", "mode": "execute"},
                {"attr": "Calibrate", "mode": "execute"},
        ]
        attributes["GalilDMCMotor"] = [ \
                {"attr": "Position", "delta": 0.1},
                {"attr": "Velocity"},
                {"attr": "Acceleration"},
                {"attr": "SoftCcwLimit", "name": "soft_limit_min"},
                {"attr": "SoftCwLimit", "name": "soft_limit_max"},
                {"attr": "SoftCcwLimitFault", "name": "soft_limit_min_fault"},
                {"attr": "SoftCwLimitFault", "name": "soft_limit_max_fault"},
                {"attr": "Stop", "name": "stop", "mode": "execute"},
                {"attr": "Calibrate", "mode": "execute"},
        ]
        attributes["OmsMaxV"] = [ \
                {"attr": "Position", "delta": 0.1},
                {"attr": "VelocityUnits", "name": "velocity"},
                {"attr": "AccelerationUnits"},
                {"attr": "SoftLimitMinUnits", "name": "soft_limit_min"},
                {"attr": "SoftLimitMaxUnits", "name": "soft_limit_max"},
                {"attr": "FlagCcwLimit", "name": "hard_limit_min_fault"},
                {"attr": "FlagCwLimit", "name": "hard_limit_max_fault"},
                {"attr": "AbortMove", "name": "stop", "mode": "execute"},
                {"attr": "Calibrate", "mode": "execute"},
                {"attr": "PIDactive", "name": "pid_active"},
        ]
        attributes["OmsVme58"] = [ \
                {"attr": "Position"},
                {"attr": "SlewRate", "name": "velocity"},
                {"attr": "Acceleration"},
                {"attr": "UnitLimitMin", "name": "soft_limit_min"},
                {"attr": "UnitLimitMax", "name": "soft_limit_max"},
                {"attr": "CcwLimit", "name": "hard_limit_min_fault"},
                {"attr": "CwLimit", "name": "hard_limit_max_fault"},
                {"attr": "StopMove", "name": "stop", "mode": "execute"},
                {"attr": "Calibrate", "mode": "execute"},
                {"attr": "Conversion"},
        ]
        attributes["PowerPMAC_Motor"] = [ \
                {"attr": "Position", "delta": 0.1},
                {"attr": "Velocity"},
                {"attr": "Acceleration"},
                {"attr": "SoftCcwLimit", "name": "soft_limit_min"},
                {"attr": "SoftCwLimit", "name": "soft_limit_max"},
                {"attr": "SoftCcwLimitFault", "name": "soft_limit_min_fault"},
                {"attr": "SoftCwLimitFault", "name": "soft_limit_max_fault"},
                {"attr": "CcwLimitFault", "name": "hard_limit_min_fault"},
                {"attr": "CwLimitFault", "name": "hard_limit_max_fault"},
                {"attr": "Stop", "name": "stop", "mode": "execute"},
                {"attr": "Calibrate", "mode": "execute"},
        ]
        attributes["Simulation"] = [ \
                {"attr": "Position"},
                {"attr": "Velocity"},
                {"attr": "Acceleration"},
                {"attr": "Soft_Limit_Min"},
                {"attr": "Soft_Limit_Max"},
                {"attr": "Stop", "mode": "execute"},
                {"attr": "Calibrate", "mode": "execute"},
        ]
        self.connector = None
        if connector == "tango":
            try:
                proxy = DeviceProxy(uri)
                type = proxy.info().dev_class
                self.type = type
                if self.type == "GalilDMCMotor" and "CwLimitFault" in \
                        proxy.get_attribute_list():
                    attributes["GalilDMCMotor"].append(
                            {"attr": "CcwLimitFault", "name": "hard_limit_min_fault"},
                            {"attr": "CwLimitFault", "name": "hard_limit_max_fault"},
                        )
            except Exception as e:
                self.janus.utils["logger"].error(
                    "TangoMotor({}).__init__() connection failed".format(self.uri))
                self.janus.utils["logger"].debug("", exc_info=True)
            if self.type in attributes:
                self.connector = TangoConnector(uri, attributes[self.type], interval=updateInterval)
        if connector == "simulation" or self.connector is None:
            self.connector = SimulationConnector(uri, attributes["Simulation"])
            self.connector.write("state", State.ON)
            if connector != "simulation":
                self.connector.write("state", State.UNKNOWN)
            self.connector.write("position", 0)
            self.connector.write("velocity", 1000)
            self.connector.write("acceleration", 1000)
            self.connector.write("soft_limit_min", 0)
            self.connector.write("soft_limit_max", 0)
        self.last_soft_limit_min_fault = \
                self.soft_limit_min_fault(refresh=True)
        self.last_soft_limit_max_fault = \
                self.soft_limit_max_fault(refresh=True)
        self.last_state = self.connector.read("state", refresh=True)
        if self.type in ["OmsMaxV", "OmsVme58", "Simulation"]:
            self.connector.value_changed.connect(self.on_value_changed)
        else:
            self.connector.value_changed.connect(self.value_changed.emit)

    def stop_device(self):
        self.connector.stop_device()

    def on_value_changed(self, attribute):
        if self.type == "OmsMaxV" and attribute in ["state", "pid_active"]:
            state = self.state()
            if state in [State.ON, State.OFF] and state != self.last_state:
                self.last_state = state
                attribute = "state"
        elif attribute in ["position", "soft_limit_min", "soft_limit_max"]:
            if self.soft_limit_min_fault() != self.last_soft_limit_min_fault:
                self.value_changed.emit("soft_limit_min_fault")
            if self.soft_limit_max_fault() != self.last_soft_limit_max_fault:
                self.value_changed.emit("soft_limit_max_fault")
        self.value_changed.emit(attribute)

    def state(self, refresh=False):
        state = self.connector.state(refresh)
        if state == State.ON and self.type == "OmsMaxV":
            pid_active = bool(self.connector.read("pid_active", refresh))
            if not pid_active:
                state = State.OFF
        return state

    def position(self, value=None, refresh=False, alt=None):
        if value is not None:
            return self.connector.write("position", float(value))
        else:
            return self.connector.read("position", refresh, alt)

    def velocity(self, value=None, refresh=False, alt=None):
        if value is not None:
            if self.type == "OmsMaxV":
                conversion = self.connector.read("conversion")
                value /= conversion
            self.connector.write("velocity", float(value))
        else:
            value =  self.connector.read("velocity", refresh)
            if value is None:
                return alt
            if self.type == "OmsMaxV":
                conversion = self.connector.read("conversion", refresh)
                value *= conversion
            return value

    def acceleration(self, value=None, refresh=False, alt=None):
        if value is not None:
            if self.type == "OmsMaxV":
                conversion = self.connector.read("conversion")
                value /= conversion
            self.connector.write("acceleration", float(value))
        else:
            value =  self.connector.read("acceleration", refresh)
            if value is None:
                return alt
            if self.type == "OmsMaxV":
                conversion = self.connector.read("conversion", refresh)
                value *= conversion
            return value

    def soft_limit_min(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("soft_limit_min", float(value))
        else:
            return self.connector.read("soft_limit_min", refresh, alt)

    def soft_limit_max(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("soft_limit_max", float(value))
        else:
            return self.connector.read("soft_limit_max", refresh, alt)

    def soft_limit_min_fault(self, refresh=False, alt=None):
        if "soft_limit_min_fault" in self.connector.attributes:
            return self.connector.read("soft_limit_min_fault", refresh)
        else:
            value = self.connector.read("soft_limit_min", refresh)
            if value == 0:
                return False
            elif value is None:
                return alt
            return value > self.connector.read("position", refresh)

    def soft_limit_max_fault(self, refresh=False, alt=None):
        if "soft_limit_max_fault" in self.connector.attributes:
            return self.connector.read("soft_limit_max_fault", refresh)
        else:
            value = self.connector.read("soft_limit_max", refresh)
            if value == 0:
                return False
            elif value is None:
                return alt
            return value < self.connector.read("position", refresh)

    def hard_limit_min_fault(self, refresh=False, alt=None):
        if "hard_limit_min_fault" in self.connector.attributes:
            return self.connector.read("hard_limit_min_fault", refresh, alt)
        else:
            return False

    def hard_limit_max_fault(self, refresh=False, alt=None):
        if "hard_limit_max_fault" in self.connector.attributes:
            return self.connector.read("hard_limit_max_fault", refresh, alt)
        else:
            return False
