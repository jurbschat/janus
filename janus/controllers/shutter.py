from abc import ABC, abstractmethod


class ShutterBase(ABC):

    def __init__(self):
        ABC.__init__()

    @abstractmethod
    def get_shutter_data(self, grid_controller):
        pass


class FullWindowShutter(ShutterBase):

    def __init__(self, points):
        ShutterBase.__init__()

    def get_shutter_data(self, grid_controller):
        return {
            "on": 12,
            "off": 7,
            "repeat": 20
        }


class WindowShutter(ShutterBase):

    def __init__(self, points):
        ShutterBase.__init__()

    def get_shutter_data(self, grid_controller):
        return {
            "what": 12,
            "ever": 7,
            "it": 20,
            "wants": 20
        }