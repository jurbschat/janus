"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-PE, P11"
__license__ = "GPL"


from PyQt5.QtCore import QObject, pyqtSignal
from ..core import Object
from ..const import State
from .connector import SimulationConnector, TangoConnector


class Device(QObject, Object):

    value_changed = pyqtSignal(str, name="valueChanged")

    def __init__(self, connector=None, uri=None, attributes=[]):
        QObject.__init__(self)
        Object.__init__(self)
        self.attributes = {}
        if connector == "simulation":
            self.connector = SimulationConnector(uri)
        elif connector == "tango":
            self.connector = TangoConnector(uri)
        self.connector.value_changed.connect(self.value_changed.emit)
        for attribute in attributes:
            self.add_attribute(attribute)
        self.add_attribute({"name": "state", \
                "attr": "State", "mode": "read", "type": State})

    def add_attribute(self, attribute):
        if type(attribute) is not dict:
            return
        if "mode" not in attribute:
            attribute["mode"] = "read"
        if "name" in attribute:
            name = attribute["name"]
        else:
            name = attribute["attr"].lower()

        def read(refresh=False, alt=None):
            return self.connector.read(name, refresh, alt)
        read.__self__ = self
        read.__name__ = name
        
        def write(value=None, refresh=False, alt=None):
            if value is not None:
                return self.connector.write(name, value)
            else:
                return self.connector.read(name, refresh, alt)
        write.__self__ = self
        write.__name__ = name

        def execute(*values):
            return self.connector.execute(name, values)
        execute.__self__ = self
        execute.__name__ = name

        self.connector.add_attribute(attribute)
        if attribute["mode"] == "read":
            setattr(self, name, read)
        elif attribute["mode"] == "write":
            setattr(self, name, write)
        elif attribute["mode"] == "execute":
            setattr(self, name, execute)
        self.attributes[name] = attribute
