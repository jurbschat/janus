"""
This is part of the janus package.
"""

__author__ = "Jan Meyer"
__email__ = "jan.meyer@desy.de"
__copyright__ = "(c)2019 DESY, FS-BMX, FS-Petra-D, P11"
__license__ = "GPL"


from time import time
from random import random
from PyQt5.QtCore import QObject, QThread, pyqtSignal, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyTango import DeviceProxy, EventType
from ..core import Object
from ..const import State, UpdatePolicy
from .devicebase import DeviceBase


class Connector(QObject, Object, DeviceBase):
    """A Connector object interfaces between devices and control systems.
    
    This is the base class to all connectors. It provides a mapping between 
    Janus attribute names and identifiers of the control system. Derived objects
    should care to keep the attribute values up to date, either by polling them
    or through event based mechanisms. A changed value should be indicated by
    a value_changed signal.
    """

    def __init__(self, uri=None, attributes=[], policy=UpdatePolicy.POLLING, interval=1.0):
        """Construct a new Connector instance.
        
        :param uri: URI to the exposed control system object.
        :type uri: str
        :param attributes: List of attributes (see add_attribute).
        :type attribute: list
        :param policy: Defines how the attributes should be updated. Defaults
            to POLLING.
        :type policy: UpdatePolicy
        :param interval: Defines the update interval in s if policy is POLLING.
        :type interval: float
        """
        QObject.__init__(self)
        Object.__init__(self)
        self.uri = uri
        self.attributes = {}
        for attribute in attributes:
            self.add_attribute(attribute)
        self.add_attribute( \
                {"name": "state", "attr": "State", "value": State.UNKNOWN})
        self.update_policy(policy, interval)

    def add_attribute(self, attribute=None):
        """Add another attribute to the Connector object.
        
        If attribute is not of type dict or doesn't contain the key attr it is 
        ignored.
        
        :param attribute: A dict describing the attribute to add. May contain:
            - name (str): The Janus identifier, defaults to lower(attr).
            - attr (str): The identifier on the control systems side.
            - mode (str): "read", "write" or "execute", defaults to "read".
            - type (type): The Python type, optional.
            - delta (float): A delta value for floating point attributes. If
                this is bigger then the difference of the current value, the
                value_changed signal is fired.
        :type attribute: dict
        """
        if type(attribute) is not dict or "attr" not in attribute:
            return
        if "name" in attribute:
            name = attribute["name"]
        else:
            name = attribute["attr"].lower()
        if name not in self.attributes:
            self.attributes[name] = {"value": None}
        for key, value in attribute.items():
            if key != "name":
                self.attributes[name][key] = value
    
    def update_policy(self, policy=UpdatePolicy.POLLING, interval=1.0):
        """Set the update policy for the attributes of this connector.

        :param policy: Defines how the attributes should be updated. Defaults
            to POLLING.
        :type policy: UpdatePolicy
        :param interval: Defines the update interval in s if policy is POLLING.
        :type interval: float
        """
        self.policy = policy
        self.interval = interval
    
    def state(self, refresh=False):
        """Return the device state.
        
        :param refresh: If set to True, the state will be queried from the
            device directly. Otherwise, a buffered value might be used.
        :type refresh: bool
        :return: The device state. Defaults to UNKNOWN if not connected.
        :rtype: State
        """
        return self.attributes["state"]["value"]

    def read(self, attribute=None, refresh=False, alt=None):
        """Get the value of the given device's attribute. 
        
        :param attribute: The name of the attribute to read.
        :type attribute: str
        :param refresh: If set to True, the value will be queried from the
            device directly. Otherwise, a buffered value might be used.
        :type refresh: bool
        :param alt: The value to return if reading fails.
        :type alt: arbitrary
        :return: The value of the given attribute, defaults to alt.
        :rtype: arbitrary
        """
        return self.attributes[attribute]["value"]
    
    def write(self, attribute=None, value=None):
        """Set the value of the given device's attribute. 
        
        :param attribute: The name of the attribute to write.
        :type attribute: str
        :param value: The value to write.
        :type value: arbitrary
        :return: False on errors, True on success.
        :rtype: bool
        """
        self.attributes[attribute]["value"] = value
        return True

    def execute(self, command=None, *values):
        """Execute a command on the device.
        
        :param command: The name of the command to execute.
        :type command: str
        :param values: If any values are given, they are passed over to the
            command as parameters..
        :type values: arbitrary
        :return: If the command returns any value, it it passed back..
        :rtype: arbitrary
        """
        pass


class SimulationConnector(Connector):

    value_changed = pyqtSignal(str, name="valueChanged")
    
    def __init__(self, uri=None, attributes=[], policy=UpdatePolicy.POLLING, interval=1.0):
        Connector.__init__(self, uri, attributes, policy, interval)

    def add_attribute(self, attribute=None):
        Connector.add_attribute(self, attribute=attribute)
        if type(attribute) is not dict or "attr" not in attribute:
            return
        if "mode" in attribute and attribute["mode"] == "execute":
            return
        if "name" in attribute:
            name = attribute["name"]
        else:
            name = attribute["attr"].lower()
        if "type" in attribute:
            if attribute["type"] == float:
                self.attributes[name]["value"] = 0.0
            elif attribute["type"] == int:
                self.attributes[name]["value"] = 0
            elif attribute["type"] == bool:
                self.attributes[name]["value"] = False
            elif attribute["type"] == str:
                self.attributes[name]["value"] = "empty"
            elif attribute["type"] == State:
                self.attributes[name]["value"] = State.ON
            else:
                self.attributes[name]["value"] = random()

    def write(self, attribute=None, value=None):
        if attribute in self.attributes.keys():
            self.attributes[attribute]["value"] = value
            if self.policy != UpdatePolicy.NO:
                self.value_changed.emit(self.attributes[attribute]["name"])
            return True
        return False


class VimbaCameraSimulationConnector(Connector):
    class AttrValue:
        def __init__(self):
            self.value = None

    class AttrEvent:
        def __init__(self):
            self.attr_name = ""
            #self.attr_value = VimbaCameraSimulationConnector.AttrValue()
            self.event = ""

    value_changed = pyqtSignal(str, name="valueChanged")
    image_changed = pyqtSignal(AttrEvent, name="imageChanged")

    def __init__(self, uri=None, attributes=[], policy=UpdatePolicy.POLLING, interval=1.0):
        Connector.__init__(self, uri, attributes, policy, interval)
        for name in self.attributes:
            self.attributes[name]["value"] = random()
        self.image = QPixmap("test_beam.png")
        self.timer = QTimer()
        self.timer.timeout.connect(self.image_update)
        self.timer.start(1000 / 1)

    def image_update(self):
        self.attributes["image_8"]["value"] = self.image
        event = VimbaCameraSimulationConnector.AttrEvent()
        event.attr_name = "image_8"
        event.event = "data_ready"
        self.image_changed.emit(event)

    def add_attribute(self, attribute=None):
        Connector.add_attribute(self, attribute=attribute)
        if type(attribute) is not dict or "attr" not in attribute:
            return
        if "mode" in attribute and attribute["mode"] == "execute":
            return
        if "name" in attribute:
            name = attribute["name"]
        else:
            name = attribute["attr"].lower()
        self.attributes[name]["value"] = random()

    def state(self, refresh=False):
        return State.ON

    def read(self, attribute=None, refresh=False, alt=None):
        return self.attributes[attribute]["value"]

    def write(self, attribute=None, value=None):
        if attribute in self.attributes.keys():
            self.attributes[attribute]["value"] = value
        if self.policy != UpdatePolicy.NO:
            self.value_changed.emit(self.attributes[attribute]["attr"])


class TangoConnector(QThread, Connector):

    value_changed = pyqtSignal(str, name="valueChanged")

    def __init__(self, uri=None, attributes=[], policy=UpdatePolicy.POLLING, interval=1.0):
        QThread.__init__(self)
        self.alive = False
        self.connected = False
        self.poll_attributes = {}
        try:
            self.proxy = DeviceProxy(uri)
            self.connected = True
        except:
            self.attributes["state"]["value"] = State.UNKNOWN
            self.janus.utils["logger"].error(
                    "TangoConnector(" + self.uri + ").__init__() " +
                    "connection failed")
            self.janus.utils["logger"].debug("", exc_info=True)
        Connector.__init__(self, uri, attributes, policy, interval)

    def add_attribute(self, attribute=None):
        Connector.add_attribute(self, attribute=attribute)
        if type(attribute) is not dict or "attr" not in attribute:
            return
        if "mode" in attribute and attribute["mode"] == "execute":
            return
        if "name" in attribute:
            name = attribute["name"]
        else:
            name = attribute["attr"].lower()
        self.poll_attributes[attribute["attr"]] = name

    def update_policy(self, policy=UpdatePolicy.POLLING, interval=1.0):
        self.interval = interval
        if policy != UpdatePolicy.POLLING and self.isRunning():
            self.stop()
        elif policy != UpdatePolicy.EVENTBASED:
            for attr in self.attributes.keys():
                if "event" not in self.attributes[attr]:
                    continue
                try:
                    self.proxy.unsubscribe_event(self.attributes[attr]["event"])
                except:
                    self.janus.utils["logger"].error(
                            "TangoConnector(" + self.uri + ").update_policy() " +
                            "failed to unsubscribe from tango event")
                    self.janus.utils["logger"].debug("", exc_info=True)
                del self.attributes[attr]["event"]
        if policy == UpdatePolicy.POLLING and not self.isRunning():
            self.start()
        elif policy == UpdatePolicy.EVENTBASED:
            for attr in self.attributes.keys:
                try:
                    self.attributes[attr]["event"] = \
                        self.proxy.subscribe_event(EventType.CHANGE_EVENT, \
                                self.on_tango_event, [], False)
                except:
                    self.janus.utils["logger"].error(
                            "TangoConnector(" + self.uri + ").update_policy() " +
                            "failed to subscribe to tango event")
                    self.janus.utils["logger"].debug("", exc_info=True)
        self.policy = policy

    def on_tango_event(self, event):
        try:
            name = event.attr_name
            value = event.attr_value.value
        except:
            self.janus.utils["logger"].warning(
                    "TangoConnector(" + self.uri + ").on_tango_event() " +
                    "invalid tango event type")
            self.janus.utils["logger"].debug("", exc_info=True)
        self.attributes[self.poll_attributes[name]]["value"] = value
        self.value_changed.emit(self.poll_attributes[name])

    def stop_device(self):
        self.stop()
        
    def stop(self):
        self.alive = False
        self.wait()

    def run(self):
        self.alive = True
        while self.alive:
            #remember when we started
            timestamp = time()
            #try to poll attributes
            try:
                attrs = self.proxy.read_attributes(list(self.poll_attributes.keys()))
            except:
                self.attributes["state"]["value"] = State.UNKNOWN
                self.janus.utils["logger"].error(
                        "TangoConnector(" + self.uri + ").run() " +
                        "reading tango attributes failed")
                self.janus.utils["logger"].debug("", exc_info=True)
                attrs = []
            #assign attribute values and fire change signal if necessary
            for attr in attrs:
                name = self.poll_attributes[attr.name]
                changed = False
                if "delta" in self.attributes[name]:
                    if self.attributes[name]["value"] is None or \
                            abs(self.attributes[name]["value"] - attr.value) > \
                            self.attributes[name]["delta"]:
                        changed = True
                elif name == "state" and \
                        int(self.attributes[name]["value"]) != int(attr.value):
                    changed = True
                elif self.attributes[name]["value"] != attr.value:
                    changed = True
                if changed:
                    if name == "state":
                        self.attributes[name]["value"] = State(int(attr.value))
                    else:
                        self.attributes[name]["value"] = attr.value
                    self.value_changed.emit(name)
                if not self.alive:
                    break
            #wait for the rest of the polling interval
            interval = int((self.interval - (time() - timestamp)) * 1000)
            while interval > 0:
                if interval > 50:
                    self.msleep(50)
                    interval -= 50
                else:
                    self.msleep(interval)
                    interval = 0
                if not self.alive:
                    break

    def state(self, refresh=False):
        if refresh:
            try:
                self.attributes["state"]["value"] = State(int(self.proxy.state()))
            except:
                self.attributes["state"]["value"] = State.UNKNOWN
                self.janus.utils["logger"].error(
                        "TangoConnector(" + self.uri + ").state() " +
                        "reading tango state failed")
                self.janus.utils["logger"].debug("", exc_info=True)
        return self.attributes["state"]["value"]

    def read(self, attribute=None, refresh=False, alt=None):
        if refresh or self.attributes[attribute]["value"] is None:
            try:
                self.attributes[attribute]["value"] = \
                    self.proxy.read_attribute(self.attributes[attribute]["attr"]).value
            except:
                self.janus.utils["logger"].error(
                        "TangoConnector(" + self.uri + ")" +
                        ".read(" + attribute + ") " +
                        "reading tango attribute failed")
                self.janus.utils["logger"].debug("", exc_info=True)
                if self.attributes[attribute]["value"] is None \
                        and alt is not None:
                    return alt
        return self.attributes[attribute]["value"]
    
    def write(self, attribute=None, value=None):
        try:
            self.proxy.write_attribute(self.attributes[attribute]["attr"], value)
            return True
        except:
            self.janus.utils["logger"].error(
                    "TangoConnector(" + self.uri + ")" +
                    ".write(" + attribute + ") " +
                    "writing tango attribute failed")
            self.janus.utils["logger"].debug("", exc_info=True)
            return False
    
    def execute(self, command=None, *values):
        try:
            if len(values) == 0:
                value = self.proxy.command_inout(self.attributes[command]["attr"])
            else:
                value = self.proxy.command_inout(self.attributes[command]["attr"], values)
        except Exception as e:
            self.janus.utils["logger"].error(
                    "TangoConnector(" + self.uri + ")" +
                    ".execute(" + command + ") " +
                    "executing tango command failed")
            self.janus.utils["logger"].debug("", exc_info=True)
            return None
        return value

