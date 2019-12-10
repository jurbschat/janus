"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-BMX, FS-Petra-D, P11"
__license__ = "GPL"


from PyQt5.QtCore import QObject, pyqtSignal
from ..core import Object
from ..const import State
from .connector import SimulationConnector, TangoConnector
from .devicebase import DeviceBase


class Xspress3(QObject, Object, DeviceBase):

    value_changed = pyqtSignal(str, name="valueChanged")

    def __init__(self, connector=None, uri=None, updateInterval = 0.5):
        QObject.__init__(self)
        Object.__init__(self)
        self.uri = uri
        self.attributes = [ \
            {"attr": "State", "name": "state", "mode": "read", "type": State},
            {"attr": "ExposureTime", "name": "exposure_time", "mode": "write", "type": float},
            {"name": "bin_width", "mode": "read", "type": float},
            {"name": "bin_energies", "mode": "read", "type": list},
            {"attr": "NbFrames", "name": "frames", "mode": "write", "type": int},
            {"attr": "TriggerMode", "name": "trigger_mode", "mode": "write", "type": int},
            {"attr": "FileDir", "name": "file_dir", "mode": "write", "type": str},
            {"attr": "FilePrefix", "name": "file_name", "mode": "write", "type": str},
            {"attr": "LastFrame", "name": "last_frame", "mode": "read", "type": int},
            {"name": "channel1", "mode": "read", "type": list},
            {"name": "channel2", "mode": "read", "type": list},
            {"name": "channel3", "mode": "read", "type": list},
            {"name": "channel4", "mode": "read", "type": list},
            {"attr": "StartAcquisition", "name": "start_acquisition", "mode": "execute"},
            {"attr": "StopAcquisition", "name": "stop_acquisition", "mode": "execute"},
        ]
        self.channels = 0
        self.connector = None
        if connector == "tango":
            self.connector = TangoConnector(uri, \
                    self.attributes, interval=updateInterval)
            try:
                attributes = self.connector.proxy.get_attribute_list()
            except Exception:
                self.janus.utils["logger"].error(
                    "Xspress3({}).__init__() connection failed".format(self.uri))
                self.janus.utils["logger"].debug("", exc_info=True)
            if "DataCh3" in attributes:
                self.channels = 4
            elif "DataCh2" in attributes:
                self.channels = 3
            elif "DataCh1" in attributes:
                self.channels = 2
            elif "DataCh0" in attributes:
                self.channels = 1
            for i in range(self.channels, 0, -1):
                del self.attributes[-1]
                delattr(self, "channel" + str(i))
        if connector == "simulation" or self.connector is None:
            self.connector = SimulationConnector(uri, self.attributes)
            if connector != "simulation":
                self.connector.write("state", State.UNKNOWN)
            self.connector.write("position", 0)
            self.connector.write("velocity", 1000)
            self.connector.write("acceleration", 1000)
            self.connector.write("soft_limit_min", 0)
            self.connector.write("soft_limit_max", 0)
        self.connector.value_changed.connect(self.value_changed.emit)

    def start_acquisition(self):
        self.connector.execute("start_acquisition")

    def stop_acquisition(self):
        self.connector.execute("stop_acquisition")

    def on_value_changed(self, attribute):
        if attribute == "last_frame":
            self.value_changed.emit("channel1")
            self.value_changed.emit("channel2")
            self.value_changed.emit("channel3")
            self.value_changed.emit("channel4")
        else:
            self.value_changed.emit(attribute)

    def state(self, refresh=False):
        return self.connector.state(refresh)
    
    def exposure_time(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("exposure_time", value)
        else:
            return self.connector.read("exposure_time", refresh, alt)

    def bin_width(self, refresh=True, alt=None):
        return 6.25 #eV

    def bin_energies(self, refresh=True, alt=None):
        width = self.bin_width()
        return [b * width + width / 2 for b in range(4096)]

    def frames(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("frames", int(value))
        else:
            return self.connector.read("frames", refresh, alt)

    def trigger_mode(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("trigger_mode", int(value))
        else:
            return self.connector.read("trigger_mode", refresh, alt)

    def file_dir(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("file_dir", value)
        else:
            return self.connector.read("file_dir", refresh, alt)

    def file_name(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("file_name", value)
        else:
            return self.connector.read("file_name", refresh, alt)

    def _channel(self, i, alt=None):
        if type(self.connector) == TangoConnector:
            try:
                return self.connector.proxy.read_attribute( \
                        "DataCh" + str(i - 1))
            except:
                self.janus.utils["logger"].error(
                    "Xspress3(" + self.uri + ").channel" + str(i) +
                    "() reading tango attribute failed")
                self.janus.utils["logger"].debug("", exc_info=True)
        if alt is None:
            return 4096*[0.0]
        else:
            return alt

    def channel1(self, refresh=True, alt=None):
        return self._channel(1, alt)

    def channel2(self, refresh=True, alt=None):
        return self._channel(2, alt)

    def channel3(self, refresh=True, alt=None):
        return self._channel(3, alt)

    def channel4(self, refresh=True, alt=None):
        return self._channel(4, alt)

