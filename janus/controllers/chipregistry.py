from janus.utils.xmlchipparser import XmlChipReadWrite
from janus.controllers.controllerbase import ControllerBase
from janus.utils.config import Config
from janus.core import Object
import glm
import re

class ParseHelper:
    @staticmethod
    def parse(str):
        str = "".join(str.split())
        pattern = re.compile(r"\((?P<x>.*?),(?P<y>.*?)\)")
        match = pattern.match(str)
        return glm.vec2(float(match.group("x")), float(match.group("y")))

    @staticmethod
    def serialize(vec):
        return "({}, {})".format(vec.x, vec.y)

class Chip():
    @staticmethod
    def get_window_count(chip):
        return chip.chip_size / (chip.window_size + chip.support_size)

    @staticmethod
    def parse(dict):
        c = Chip()
        c.name = dict["name"]
        c.origin_offset = ParseHelper.parse(dict["origin_offset"])
        c.chip_size = ParseHelper.parse(dict["chip_size"])
        c.hole_distance = ParseHelper.parse(dict["hole_distance"])
        c.odd_indentation = float(dict["odd_indentation"])
        c.window_size = ParseHelper.parse(dict["window_size"])
        c.support_size = ParseHelper.parse(dict["support_size"])
        return c

    @staticmethod
    def serialize(chip):
        return {
            "origin_offset": ParseHelper.serialize(chip.origin_offset),
            "chip_size": ParseHelper.serialize(chip.chip_size),
            "hole_distance": ParseHelper.serialize(chip.hole_distance),
            "odd_indentation": chip.odd_indentation,
            "window_size": ParseHelper.serialize(chip.window_size),
            "support_size": ParseHelper.serialize(chip.support_size),
        }

    def __init__(self):
        self.name = "INVALID"
        self.origin_offset = glm.vec2(0, 0)
        self.chip_size = glm.vec2(0, 0)
        self.hole_distance = glm.vec2(0, 0)
        self.odd_indentation = 0
        self.window_size = glm.vec2(0, 0)
        self.support_size = glm.vec2(0, 0)

class ChipRegistry(ControllerBase, Object):
    def __init__(self, path):
        Object.__init__(self)
        self.path = path
        #self.chip_handler = XmlChipReadWrite(path)
        self.config = self.janus.utils["config"]

    def update_chip(self, chip):
        section_name = "chip-{}".format(chip.name)
        chip_dict = Chip.serialize(chip)
        for prop_name, prop_val in chip_dict.items():
            self.config.set(section_name, "{}".format(prop_name), str(prop_val))

    def get_chip(self, name):
        section_name = "chip-{}".format(name)
        section = self.config.items(section_name)
        chip_dict = dict(section)
        chip_dict["name"] = name
        return Chip.parse(chip_dict)

    def get_chip_list(self):
        list = []
        for section_name in self.config.sections():
            if section_name.startswith("chip-"):
                list.append(section_name[len("chip-"):])
        return sorted(list)