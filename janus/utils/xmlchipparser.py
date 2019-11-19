import xml.etree.ElementTree as ET
import collections

class Chip():
    def __init__(self):
        self.chip_name = "INVALID"
        self.chip_width = 0
        self.chip_height = 0
        self.window_width = 0
        self.window_height = 0
        self.gap_width = 0
        self.gap_height = 0
        self.horizontal_pitch = 0
        self.vertical_pitch = 0
        self.top_left_linear = 0
        self.top_left_y = 0
        self.num_horizontal_windows = 0
        self.triangular = 1

class XmlChipReadWrite:
    def __init__(self, path):
        self.name_mapping = {
            "chip_name": "name",
            "chip_width": "chipWidth",
            "chip_height": "chipHeight",
            "window_width": "windowWidth",
            "window_height": "windowHeight",
            "gap_width": "gapWidth",
            "gap_height": "gapHeight",
            "horizontal_pitch": "horizontalPitch",
            "vertical_pitch": "verticalPitch",
            "top_left_linear": "topLeftLinear",
            "top_left_y": "topLeftY",
            "num_horizontal_windows": "numHorizontalWindows",
            "triangular": "triangular"
        }
        self.chips = self.parse(path)

    def parse(self, path):
        chips_dict = {}
        et = ET.parse('chips.xml')
        root = et.getroot()
        for child in root:
            chip = Chip()
            chip.chip_name = str(child.get(self.name_mapping["chip_name"]))
            chip.chip_width = float(child.find(self.name_mapping["chip_width"]).text)
            chip.chip_height = float(child.find(self.name_mapping["chip_height"]).text)
            chip.window_width = float(child.find(self.name_mapping["window_width"]).text)
            chip.window_height = float(child.find(self.name_mapping["window_height"]).text)
            chip.gap_width = float(child.find(self.name_mapping["gap_width"]).text)
            chip.gap_height = float(child.find(self.name_mapping["gap_height"]).text)
            chip.horizontal_pitch = float(child.find(self.name_mapping["horizontal_pitch"]).text)
            chip.vertical_pitch = float(child.find(self.name_mapping["vertical_pitch"]).text)
            chip.top_left_linear = float(child.find(self.name_mapping["top_left_linear"]).text)
            chip.top_left_y = float(child.find(self.name_mapping["top_left_y"]).text)
            chip.num_horizontal_windows = int(child.find(self.name_mapping["num_horizontal_windows"]).text)
            chip.triangular = int(child.find(self.name_mapping["triangular"]).text)
            chips_dict[chip.chip_name] = chip
        return collections.OrderedDict(sorted(chips_dict.items()))

    def write_changes(self, chips, path):
        xml_chips = ET.Element("chips")
        for name, chip in chips.items():
            xml_chip = ET.Element('chip', name=name)
            for name, prop in chip.__dict__.items():
                xml_prop = ET.Element(self.name_mapping[name])
                xml_prop.text = prop
                xml_chip.extend(xml_prop)
            xml_chips.extend(xml_chip)

    def get_chips(self):
        return self.chips

