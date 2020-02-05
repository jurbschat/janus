'''
Created on May 6, 2019

@author: janmeyer
'''

from ..core import Object
from ..const import State
from .connector import SimulationConnector, TangoConnector, VimbaCameraSimulationConnector
from .devicebase import DeviceBase
from time import sleep
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QImage
from PyTango import Database, EventType, ExtractAs


class Camera(QObject, Object, DeviceBase):

    def __init__(self):
        QObject.__init__(self)
        Object.__init__(self)
        self.attributes = { \
            "state": {"mode": "read", "type": State},
            "exposure_time": {"mode": "write", "type": float},
            "exposure_time_min": {"mode": "write", "type": float},
            "exposure_time_max": {"mode": "write", "type": float},
            "exposure_time_auto": {"mode": "write", "type": bool},
            "gain": {"mode": "write", "type": float},
            "gain_min": {"mode": "write", "type": float},
            "gain_max": {"mode": "write", "type": float},
            "gain_auto": {"mode": "write", "type": bool},
            "width_max": {"mode": "write", "type": float},
            "height_max": {"mode": "write", "type": float},
            "size": {"mode": "write", "type": tuple},
        }

    def state(self, refresh=False):
        return self.connector.state(refresh)

    def exposure_time(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("exposure_time", int(value))
        else:
            return self.connector.read("exposure_time", refresh, alt)

    def exposure_time_min(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("exposure_time_min", int(value))
        else:
            return self.connector.read("exposure_time_min", refresh, alt)

    def exposure_time_max(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("exposure_time_max", int(value))
        else:
            return self.connector.read("exposure_time_max", refresh, alt)

    def exposure_time_auto(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("exposure_time_auto", bool(value))
        else:
            return self.connector.read("exposure_time_auto", refresh, alt)

    def gain(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("gain", int(value))
        else:
            return self.connector.read("gain", refresh, alt)

    def gain_min(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("gain_min", int(value))
        else:
            return self.connector.read("gain_min", refresh, alt)

    def gain_max(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("gain_max", int(value))
        else:
            return self.connector.read("gain_max", refresh, alt)

    def gain_auto(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("gain_auto", int(value))
        else:
            return self.connector.read("gain_auto", refresh, alt)

    def frame_rate(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("frame_rate", int(value))
        else:
            return self.connector.read("frame_rate", refresh, alt)

    def width_max(self, refresh=False, alt=None):
        return self.connector.read("width_max", refresh, alt)

    def height_max(self, refresh=False, alt=None):
        return self.connector.read("height_max", refresh, alt)

    def size(self, width=None, height=None):
        pass

    def image(self):
        return self.connector.read("image")

    def stop_device(self):
        self.connector.stop_device()


class VimbaCamera(Camera):

    value_changed = pyqtSignal(str, name="valueChanged")

    def __init__(self, connector=None, uri=None):
        Camera.__init__(self)
        self.uri = uri
        attributes = [ \
                {"attr": "ExposureAuto", "name": "exposure_time_auto"},
                {"attr": "ExposureAutoMin", "name": "exposure_time_min"},
                {"attr": "ExposureAutoMax", "name": "exposure_time_max"},
                {"attr": "ExposureTimeAbs", "name": "exposure_time"},
                {"attr": "GainAuto", "name": "gain_auto"},
                {"attr": "GainAutoMin", "name": "gain_min"},
                {"attr": "GainAutoMax", "name": "gain_max"},
                {"attr": "Gain", "name": "gain"},
                {"attr": "TriggerSource", "name": "trigger_source"},
                {"attr": "AcquisitionFrameRateAbs", "name": "frame_rate"},
                {"attr": "Width"},
                {"attr": "Height"},
                {"attr": "OffsetX", "name": "offset_x"},
                {"attr": "OffsetY", "name": "offset_y"},
                {"attr": "WidthMax", "name": "width_max"},
                {"attr": "HeightMax", "name": "height_max"},
                {"attr": "Image8", "name": "image_8"},
        ]
        if connector == "simulation":
            attributes.append({"attr": "Image8", "name": "image_8"})
            self.connector = VimbaCameraSimulationConnector(uri, attributes)
            self.connector.write("width", 640)
            self.connector.write("height", 480)
            self.connector.write("width_max", 640)
            self.connector.write("height_max", 480)
            self.connector.image_changed.connect(self.on_image_changed)
        elif connector == "tango":
            #determine gain attribute name
            if -1 < uri.find(":") < uri.find("/"):
                host, port = uri.partition("/")[0].split(":")
                db = Database(host, port)
                gain_prop = db.get_device_property(
                        uri.partition("/")[2], "GainFeatureName")
            else:
                db = Database()
                gain_prop = db.get_device_property(uri, "GainFeatureName")
            if len(gain_prop["GainFeatureName"]) > 0:
                gain_attr = gain_prop["GainFeatureName"][0]
                for attr in attributes:
                    if "name" in attr and attr["name"] == "gain":
                        attr["attr"] = gain_attr
            #setup connector
            self.connector = TangoConnector(uri, attributes)
            #start acquisition in right viewing mode and connect changed signal
            try:
                self.connector.proxy.write_attribute("ViewingMode", 1)
                if self.state(refresh=True) != State.RUNNING:
                    self.connector.proxy.command_inout("StartAcquisition")
                sleep(0.2)
                self.connector.proxy.subscribe_event("image_8", \
                        EventType.DATA_READY_EVENT, \
                        self.on_image_changed, [], False)
            except:
                self.janus.utils["logger"].error(
                        "VimbaCamera(" + self.uri + ").__init__() " +
                        "failed to set viewing mode")
                self.janus.utils["logger"].debug("", exc_info=True)
        self.connector.write("trigger_source", "FixedRate")
        self.connector.write("frame_rate", 10.)
        self.connector.value_changed.connect(self.value_changed.emit)
        self.buffer = None

    def on_image_changed(self, event):
        try:
            name = event.attr_name.lower()
            n = name.rfind("/")
            if n > 0:
                name = name[n+1:]
                event_type = event.event
            if name == "image_8" and event.event == "data_ready":
                self.buffer = QImage(self.connector.read("image_8"))
                self.value_changed.emit("image")
            if name == "imageenc" and event_type == "data_ready":
                value = self.connector.proxy.read_attribute("ImageEnc", extract_as=ExtractAs.ByteArray).value[1]
                self.buffer = QImage.fromData(value)
                self.value_changed.emit("image")
        except:
            self.janus.utils["logger"].warning(
                    "VimbaCamera(" + self.uri + ").on_image_changed() " +
                    "failed to read image or invalid tango event type")
            self.janus.utils["logger"].debug("", exc_info=True)

    def exposure_time_auto(self, value=None, refresh=False, alt=None):
        if value is None:
            auto = self.connector.read("exposure_time_auto", refresh)
            if auto == "Off":
                return False
            elif auto == "Continuous":
                return True
            elif alt is not None:
                return alt
            else:
                return None
        elif bool(value) == True:
            self.connector.write("exposure_time_auto", "Continuous")
        elif bool(value) == False:
            self.connector.write("exposure_time_auto", "Off")

    def gain_auto(self, value=None, refresh=False, alt=None):
        if value is None:
            auto = self.connector.read("gain_auto", refresh)
            if auto == "Off":
                return False
            elif auto == "Continuous":
                return True
            elif alt is not None:
                return alt
            else:
                return None
        elif bool(value) == True:
            self.connector.write("gain_auto", "Continuous")
        elif bool(value) == False:
            self.connector.write("gain_auto", "Off")

    def frame_rate(self, value=None, refresh=False, alt=None):
        if value is not None:
            self.connector.write("frame_rate", int(value))
            self.connector.write("trigger_source", "FixedRate")
        else:
            return self.connector.read("frame_rate", refresh, alt)

    def size(self, value=None, refresh=False, alt=None):
        if value is None:
            return (self.connector.read("width", refresh),
                    self.connector.read("height", refresh))
#         try:
#             width = value[0]
#             height = value[1]
#         except:
#             self.janus.utils["logger"].error( \
#                     "Vimba(" + self.uri + ").size()" +
#                     "invalid parameter"
#                 )
#             return
#         if width == 0 and height == 0:
#             width = self.connector.read("widthmax")
#             height = self.connector.read("heightmax")
#         width = min(self.widthMax - 2 * abs(self.offsetX), width)
#         height = min(self.heightMax - 2 * abs(self.offsetY), height)
#         posX = max((self.widthMax - 2 * abs(self.offsetX) - width) / 2., 0)
#         posY = max((self.heightMax - 2 * abs(self.offsetY) - height) / 2., 0)
#         if self.offsetX > 0.0:
#             posX += 2 * self.offsetX
#         if self.offsetY > 0.0:
#             posY += 2 * self.offsetY
#         self.width = width
#         self.height = height
#         self.camera.sendCmd(1, MjpgStream.IN_CMD_AVT_BINNING_X)
#         self.camera.msleep(10)
#         self.camera.sendCmd(1, MjpgStream.IN_CMD_AVT_BINNING_Y)
#         self.camera.msleep(10)
#         if int(posX) == 0:
#             self.camera.sendCmd(int(posX), MjpgStream.IN_CMD_AVT_REGION_X)
#             self.camera.msleep(10)
#         if int(posY) == 0:
#             self.camera.sendCmd(int(posY), MjpgStream.IN_CMD_AVT_REGION_Y)
#             self.camera.msleep(10)
#         self.camera.sendCmd(int(width), MjpgStream.IN_CMD_AVT_WIDTH)
#         self.camera.msleep(10)
#         self.camera.sendCmd(int(height), MjpgStream.IN_CMD_AVT_HEIGHT)
#         self.camera.msleep(10)
#         if int(posX) > 0:
#             self.camera.sendCmd(int(posX), MjpgStream.IN_CMD_AVT_REGION_X)
#             self.camera.msleep(10)
#         if int(posY) > 0:
#             self.camera.sendCmd(int(posY), MjpgStream.IN_CMD_AVT_REGION_Y)

    def image(self):
        return self.buffer
