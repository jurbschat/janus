from PyQt5.QtCore import *
import math

def get_window_shutter_data(grid_controller):
    #rows = chip.chip_size.x()
    #chip.hole_distance
    #chip.odd_indentation
    #chip.window_size
    #chip.support_size
    chip = grid_controller.chip
    window_with_support_size = (chip.window_size + chip.support_size)
    window_and_support_rows = window_with_support_size.x() / chip.hole_distance.x()
    window_and_support_columns = window_with_support_size.y() / chip.hole_distance.y()


    return {
        "start": QPointF(0, 0),
        "end": QPointF(0, 0),
        "on": 12,
        "off": 7,
        "repeats": 9
    }

def get_full_window_shutter_data(grid_controller):
    '''if len(grid_controller.lines) == 0:
        return {"on": 0, "off": 0, "repeats": 0}
    line = grid_controller.lines[0]


    # first and last index are always invalid as those belong to the outer border
    is_active = False
    repeats = 0
    window_size = 0
    start = line["startIdx"]
    end = line["endIdx"]
    for idx in range(start + 1, end):
        is_valid = grid_controller.meta[idx]["valid"]
        if window_size == 0 and is_valid == False:
            window_size = line["startIdx"] - idx


    shutter_lines = {
        "on": chip.window_size.x() / chip.hole_distance.x(),
        "off": chip.support_size.x() / chip.hole_distance.x(),
        "repeats": repeats,
        #"lines": lines
    }'''
    return None
