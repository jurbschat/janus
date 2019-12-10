"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-BMX, FS-Petra-D, P11"
__license__ = "GPL"


from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal
from ..core import Object
from ..const import State
from .connector import SimulationConnector, TangoConnector


class P11Shutter(QObject, Object):

    value_changed = pyqtSignal(str, name="valueChanged")

    def __init__(self, connector=None, uri=None):
        QObject.__init__(self)
        Object.__init__(self)
        self.attributes = [
            {"attr": "State", "name": "state", "mode": "read", "type": State},
            {"attr": "Value", "name": "value", "mode": "write", "type": bool},
            {"name": "open", "mode": "execute"},
            {"name": "close", "mode": "execute"}]
        if connector == "simulation":
            self.connector = SimulationConnector(uri, self.attributes)
        elif connector == "tango":
            self.connector = TangoConnector(uri, self.attributes)
        self.connector.value_changed.connect(self.value_changed.emit)

    def state(self, refresh=False):
        return self.connector.state(refresh)

    def open(self):
        self.connector.write("value", True)

    def close(self):
        self.connector.write("value", False)

    def value(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("value", bool(value))
        else:
            return bool(self.connector.read("value", refresh, alt))


class P11Filters(QObject, Object):

    value_changed = pyqtSignal(str, name="valueChanged")

    def __init__(self, connector=None, uri=None):
        QObject.__init__(self)
        Object.__init__(self)
        self.attributes = [
            {"attr": "State", "name": "state", "mode": "read", "type": State},
            {"attr": "CurrentTransmission", "name": "transmission", 
                    "mode": "read", "type": float, "delta": 0.0001},
            {"attr": "SelectTransmission", "name": "transmission_set", 
                    "mode": "write", "type": float, "delta": 0.0001}]
        self.transmission_set_value = (0.0, 0.0)
        if connector == "simulation":
            self.connector = SimulationConnector(uri, self.attributes)
        elif connector == "tango":
            self.connector = TangoConnector(uri, self.attributes)
        self.connector.value_changed.connect(self.value_changed.emit)

    def state(self, refresh=False):
        return self.connector.state(refresh)

    def transmission(self, value=None, refresh=False, alt=None):
        if value is not None:
            if type(self.connector) == SimulationConnector:
                self.connector.write("transmission", float(value) / 100)
            for i in range(20):
                if self.connector.state(True) == State.ON:
                    break
                sleep(0.1)
            self.connector.write("transmission_set", float(value) / 100)
            value_set = self.connector.read("transmission_set", refresh=True) * 100
            self.transmission_set_value = (value, value_set)
        else:
            return float(self.connector.read("transmission", refresh, alt))

    def transmission_set(self, refresh=False, alt=None):
        value = self.connector.read("transmission", refresh, alt) * 100
        if value > self.transmission_set_value[1] * 0.9 and \
                value < self.transmission_set_value[1] * 1.1:
            return self.transmission_set_value[0]
        return float(self.connector.read("transmission_set", refresh, alt)) * 100

