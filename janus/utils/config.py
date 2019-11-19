'''
Created on May 24, 2019

@author: janmeyer
'''

from ..core import Object
import os
from configparser import ConfigParser
from collections import OrderedDict


class Config(ConfigParser, Object):
    
    def __init__(self, filename=None, defaults=None):
        ConfigParser.__init__(self)
        Object.__init__(self)
        self.persistent = OrderedDict()
        self.filename = filename
        if self.filename[0] != "/":
            self.filename = os.path.abspath( \
                    self.janus.application.path + "/" + self.filename)
        self.defaults = defaults
        self.load()
    
    def geturi(self, section, option):
        connectors = ["simulation", "tango"]
        value = self.get(section, option)
        for connector in connectors:
            if value.startswith(connector + "(") and value.endswith(")"):
                uri = value[len(connector) + 1:-1]
                return connector, uri
        self.janus.utils["logger"].warning(
                "Config(" + self.filename + ").geturi() " +
                "\"" + value + "\" has no connector type defined, using simulation")
        return "simulation", value

    def add_persistent(self, section, option, getter, setter, data_type=str):
        if not self.has_section(section):
            self.add_section(section)
        if not section in self.persistent:
            self.persistent[section] = OrderedDict()
        self.persistent[section][option] = [data_type, getter, setter]

    def remove_persistent(self, section, option):
        if section in self.persistent:
            self.persistent["section"].pop(option, None)
            if len(self.persistent["section"]) == 0:
                del self.persistent["section"]

    def load_persistent(self):
        if self.defaults is not None:
            self.read_dict(self.defaults)
        if not os.access(self.filename, os.R_OK):
            self.janus.utils["logger"].error(
                    "Config(" + self.filename + ").load_persistent() " +
                    "file not readable")
        else:
            self.read(self.filename)
        for section in sorted(self.persistent.keys(), key=str.lower):
            if not self.has_section(section):
                if not os.access(self.filename, os.R_OK):
                    self.janus.utils["logger"].warning(
                            "Config(" + self.filename + ").load_persistent() " +
                            "section not in settings file: "+str(section))
                continue
            for option, value in self.items(section):
                if not option in self.persistent[section]:
                    continue
                if self.persistent[section][option][0] == bool:
                    self.persistent[section][option][2]( \
                            self.getboolean(section, option))
                elif self.persistent[section][option][0] == int:
                    self.persistent[section][option][2]( \
                            self.getint(section, option))
                elif self.persistent[section][option][0] == float:
                    self.persistent[section][option][2]( \
                            self.getfloat(section, option))
                elif self.persistent[section][option][0] == str:
                    self.persistent[section][option][2]( \
                            self.get(section, option))
        self.janus.utils["logger"].info( \
                "Config(" + self.filename + ").load_persistent() " +
                "persistent settings loaded")
    
    def save_persistent(self):
        if not os.access(self.filename, os.R_OK|os.W_OK):
            self.janus.utils["logger"].error(
                    "Config(" + self.filename + ").save_persistent() " +
                    "file not read or writeable")
            return
        for section in sorted(self.persistent.keys(), key=str.lower):
            for option in self.persistent[section]:
                self.set(section, option, str( \
                    self.persistent[section][option][1]()))
        temp = {s: OrderedDict(self.items(s)) for s in self.sections()}
        self.read(self.filename)
        self.read_dict(temp)
        with open(self.filename, encoding='utf-8', mode='w') as outputfile:
            self.write(outputfile)
        self.janus.utils["logger"].info(
                "Config(" + self.filename + ").save_persistent() " +
                "persistent settings saved")

    def load(self, persistent=True):
        if self.defaults is not None:
            self.read_dict(self.defaults)
        if not os.access(self.filename, os.R_OK):
            self.janus.utils["logger"].error(
                    "Config(" + self.filename + ").load() " +
                    "file not readable")
        else:
            self.read(self.filename)
        if persistent:
            self.load_persistent()
        self.janus.utils["logger"].info(
                "Config(" + self.filename + ").load() " +
                "settings loaded")

    def save(self, persistent=True):
        if not os.access(self.filename, os.R_OK|os.W_OK):
            self.janus.utils["logger"].error(
                    "Config(" + self.filename + ").save() " +
                    "file not read or writeable")
            return
        temp = {s: OrderedDict(self.items(s)) for s in self.sections()}
        self.read(self.filename)
        self.read_dict(temp)
        with open(self.filename, encoding='utf-8', mode='w') as outputfile:
            self.write(outputfile)
        if persistent:
            self.save_persistent()
        self.janus.utils["logger"].info(
                "Config(" + self.filename + ").save() " +
                "settings saved")
