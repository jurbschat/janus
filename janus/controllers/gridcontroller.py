import os
import sys
from timeit import default_timer as timer
import numpy as np
from scipy.spatial import KDTree
from scipy.spatial import cKDTree
from janus.utils.observableproperty import ObservableProperty
from janus.controllers.controllerbase import ControllerBase
import math
import glm
import scipy
import pprint

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

def rand_cmap(nlabels, type='bright', first_color_black=True, last_color_black=False, verbose=True):
    """
    Creates a random colormap to be used together with matplotlib. Useful for segmentation tasks
    :param nlabels: Number of labels (size of colormap)
    :param type: 'bright' for strong colors, 'soft' for pastel colors
    :param first_color_black: Option to use first color as black, True or False
    :param last_color_black: Option to use last color as black, True or False
    :param verbose: Prints the number of labels and shows the colormap. True or False
    :return: colormap for matplotlib
    """
    from matplotlib.colors import LinearSegmentedColormap
    import colorsys
    import numpy as np


    if type not in ('bright', 'soft'):
        print ('Please choose "bright" or "soft" for type')
        return

    if verbose:
        print('Number of labels: ' + str(nlabels))

    # Generate color map for bright colors, based on hsv
    if type == 'bright':
        randHSVcolors = [(np.random.uniform(low=0.0, high=1),
                          np.random.uniform(low=0.2, high=1),
                          np.random.uniform(low=0.9, high=1)) for i in range(nlabels)]

        # Convert HSV list to RGB
        randRGBcolors = []
        for HSVcolor in randHSVcolors:
            randRGBcolors.append(colorsys.hsv_to_rgb(HSVcolor[0], HSVcolor[1], HSVcolor[2]))

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]

        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)
        return randRGBcolors

    # Generate soft pastel colors, by limiting the RGB spectrum
    if type == 'soft':
        low = 0.6
        high = 0.95
        randRGBcolors = [(np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high),
                          np.random.uniform(low=low, high=high)) for i in range(nlabels)]

        if first_color_black:
            randRGBcolors[0] = [0, 0, 0]

        if last_color_black:
            randRGBcolors[-1] = [0, 0, 0]
        random_colormap = LinearSegmentedColormap.from_list('new_map', randRGBcolors, N=nlabels)
        return randRGBcolors

    # Display colorbar
    if verbose:
        from matplotlib import colors, colorbar
        from matplotlib import pyplot as plt
        fig, ax = plt.subplots(1, 1, figsize=(15, 0.5))

        bounds = np.linspace(0, nlabels, nlabels + 1)
        norm = colors.BoundaryNorm(bounds, nlabels)

        cb = colorbar.ColorbarBase(ax, cmap=random_colormap, norm=norm, spacing='proportional', ticks=None,
                                   boundaries=bounds, format='%1i', orientation=u'horizontal')

    return random_colormap

class GeneratorBase:
    def get_bounding_points(self):
        return [ glm.vec2(0, 0), glm.vec2(0, 0), glm.vec2(0, 0), glm.vec2(0, 0) ]

class AABBPointGenerator(GeneratorBase):
    def __init__(self, pos, size, step_x, step_y):
        start = timer()
        print("generating points...")
        self.pos = pos
        self.size = size
        self.points, self.meta, self.lines = self.build_points_with_data(pos, size, step_x, step_y)
        end = timer()
        print("generating {} points took: {}ms".format(len(self.points), int((end - start)*1000)))

    def build_points_with_data(self, pos, size, step_x, step_y):
        points = []
        lines = []
        idx = 0
        for y in np.arange(0, self.size.y + step_y, step_y):
            startPos = glm.vec2(step_x, y)
            startIdx = idx
            p = glm.vec2()
            for x in np.arange(0, self.size.x + step_x, step_x):
                p = glm.vec2(x, y) + self.pos
                points.append((p.x, p.y))
                idx += 1
            endPos = p
            endIdx = idx - 1
            lines.append({"startPos": startPos, "startIdx": startIdx, "endPos": endPos, "endIdx": endIdx, "startEndVec": endPos - startPos })
        cmap = rand_cmap(10, first_color_black=False)
        cmap = [(i[0] * 255, i[1] * 255, i[2] * 255) for i in cmap]
        npcmap = np.array(cmap)
        lookup = np.random.randint(low = 0, high = len(npcmap) - 1, size = len(points))
        return np.array(points), np.array([[0, 255, 0]] * len(points)), np.array(lines)

    def get_bounding_points(self):
        return [
            self.pos,
            self.pos + glm.vec2(self.size.x, 0),
            self.pos + glm.vec2(self.size.x, self.size.y),
            self.pos + (0, self.size.y)
        ]

class BBPointGenerator(GeneratorBase):
    def __init__(self, bounding_points, columnSpacing, lineSpacing, evenIndentation):
        start = timer()
        print("generating points...")
        self.points, self.meta, self.lines = self.build_points_with_data(bounding_points, columnSpacing, lineSpacing, evenIndentation)
        self.bounding_points = bounding_points
        end = timer()
        print("generating {} points took: {}ms".format(len(self.points), int((end - start)*1000)))

    def build_points_with_data(self, bounding_points, columnSpacing, lineSpacing, evenIndentation):
        points = []
        lines = []
        origin = bounding_points[0]
        vecRight = bounding_points[1] - bounding_points[0]
        vecDown = bounding_points[3] - bounding_points[0]
        columns = glm.length(vecRight) / columnSpacing
        rows = glm.length(vecDown) / lineSpacing
        rightStep = glm.normalize(vecRight) * columnSpacing
        downStep = glm.normalize(vecDown) * lineSpacing
        idx = 0
        for y in np.arange(0, rows, 1):
            startPos = origin + rightStep * 0 + downStep * y
            startIdx = idx
            p = glm.vec2()
            for x in np.arange(0, columns, 1):
                p = origin + rightStep * x + downStep * y
                points.append((p.x, p.y))
                idx += 1
            endPos = p
            endIdx = idx - 1
            lines.append({"startPos": startPos, "startIdx": startIdx, "endPos": endPos, "endIdx": endIdx, "startEndVec": endPos - startPos })
        cmap = rand_cmap(10, first_color_black=False)
        cmap = [(i[0] * 255, i[1] * 255, i[2] * 255) for i in cmap]
        npcmap = np.array(cmap)
        lookup = np.random.randint(low = 0, high = len(npcmap) - 1, size = len(points))
        return np.array(points), npcmap[lookup], np.array(lines)

    def get_bounding_points(self):
        return self.bounding_points

class ChipPointGenerator(GeneratorBase):
    def __init__(self, bounding_points, chip):
        self.points = np.array([(0, 0)])
        self.meta = np.array([(255, 0, 0)])
        self.lines = []
        self.bounding_points = bounding_points
        print("generating points... ", end = "", flush=True)
        start = timer()
        self.build_points2(bounding_points, chip)
        end = timer()
        print("done. generating {} points took: {}ms".format(len(self.points), int((end - start)*1000)))

    def get_angle_from_bounding_points(self, bounding_points):
        vec = bounding_points[1] - bounding_points[0]
        angle =  math.atan2(-vec.y, vec.x) * 180 / math.pi
        return angle

    #@profile
    def build_points2(self, bounding_points, chip):
        # as floating point calculations are inherently not 100% precise it can be
        # that a rotated vector of length 500 comes out at e.g. 499.99999647, to
        # compensate this we ass a small epsilon to the length that should generally
        # not affect the whole chip size significantly but make calculations that lie
        # directly on a border (e.g. chip size is evenly divisible by hole distance)
        # more robust
        eps = 0.00001
        size_x = glm.distance(bounding_points[1], bounding_points[0]) + eps
        size_y = glm.distance(bounding_points[3], bounding_points[0]) + eps

        # generate point grind as numpy array of 2d tuples, e.g. [[], []...]
        # we use this as the point of truth for our grid size to calculate
        # rows/columns. numpy point generation is way faster that manual looping in python
        # for values > 1e6
        grid = np.mgrid[0:size_x:chip.hole_distance.x, 0:size_y:chip.hole_distance.y]
        columns = grid.shape[1]
        rows = grid.shape[2]
        points = grid.T.reshape(-1, 2)

        # translate and rotate points to match our grid transformation specified by
        # the pounding points
        vec = bounding_points[1] - bounding_points[0]
        angle = math.atan2(vec.y, vec.x)
        rot = np.array([[math.cos(angle), -math.sin(angle)], [math.sin(angle), math.cos(angle)]])
        translation = bounding_points[0]
        points = points.dot(rot.T)
        points = points + translation
        self.points = points

        # generate meta info for every point. this info will also be returned when a point query
        # is done via the controller
        meta = np.tile({"color": [0, 255, 0], "valid": False}, [rows, columns])

        # mark all rows with support structure als invalid. we do this per row
        def mark_support_structure(size, window_size, hole_distance, support_size, color):
            if support_size == 0:
                return
            structures = math.ceil(size / (window_size + support_size))
            max_row = meta.shape[0]
            for structure_id in range(structures):
                start_pos = window_size * (structure_id + 1) + support_size * structure_id
                end_pos = start_pos + support_size
                start_row = math.ceil(start_pos / hole_distance)
                end_row = math.floor(end_pos / hole_distance) + 1
                end_row = min(max_row, end_row)
                for row in range(start_row, end_row):
                    meta[row,] = {"color": color, "valid": False}

        # we mark all support rows and then transpose and repeat the step.
        # this is faster that some python logic for the columns case as
        # it runs is numpy
        mark_support_structure(size_y, chip.window_size.y, chip.hole_distance.y, chip.support_size.y, [255, 0, 0])
        meta = meta.transpose()
        mark_support_structure(size_x, chip.window_size.x, chip.hole_distance.x, chip.support_size.x, [255, 0, 0])
        meta = meta.transpose()
        meta = meta.ravel()
        self.meta = meta

        ''' # separate support structure marking into x and y as
        # it speeds up the marking by quite a margin (~factor 10)
        # for vertical support structures we check start/end of the support structure
        # in x (columns) direction and apply it to all rows, then we move to the next
        # structure in x direction
        meta = np.repeat({"color": [0, 255, 0], "valid": False}, len(points))
        col_index = 0
        while True:
            start_x = chip.window_size.x * (col_index + 1) + chip.support_size.x * col_index
            end_x = start_x + chip.support_size.x
            if start_x >= size_x:
                break
            for y_index in range(rows):
                offset = (y_index * columns)
                start_id = int(start_x / chip.hole_distance.x) + offset
                # support structure is calculated "inclusive" if a point is on the edge
                # of a structure we count it as out, therefore + 1
                end_id = int(end_x / chip.hole_distance.x) + offset + 1
                meta[start_id:end_id] = {"color": [0, 255, 255], "valid": False}
            col_index = col_index + 1

        # for horizontal support structures we check the rows that are affected and simply
        # completely mark them
        row_index = 0
        while True:
            start_y = chip.window_size.y * (row_index + 1) + chip.support_size.y * row_index
            end_y = start_y + chip.support_size.y
            start_row = int(start_y / chip.hole_distance.y)
            if start_row >= rows:
                break
            #
            affected_rows = int((end_y - start_y) / chip.hole_distance.y) + 1
            for row_offset in range(affected_rows):
                start_id = (start_row + row_offset) * columns
                end_id = start_id + (columns - 1)
                meta[start_id:end_id] = {"color": [255, 0, 255], "valid": False}
            row_index = row_index + 1
        self.meta = meta'''

        # generate line information for all points
        lines = []
        for row in range(rows):
            start = columns * row
            end = start + (columns - 1)
            entry = {
                "startPos": points[start],
                "startIdx": start,
                "endPos": points[end],
                "endIdx": end,
                "startEndVec": points[start] - points[end]
            }
            self.lines.append(self.lines.append(entry))
        self.lines = np.array(lines)

    def build_points(self, bounding_points, chip):
        points = []
        lines = []
        origin = bounding_points[0]
        vec_right = bounding_points[1] - bounding_points[0]
        vec_down = bounding_points[3] - bounding_points[0]
        columns = glm.length(vec_right) / chip.hole_distance.x
        rows = glm.length(vec_down) / chip.hole_distance.y
        right_step = glm.normalize(vec_right) * chip.hole_distance.x
        down_step = glm.normalize(vec_down) * chip.hole_distance.y
        odd_line_offset = glm.normalize(vec_right) * chip.odd_indentation
        line_length_with_offset = right_step * columns + down_step * 0 + odd_line_offset
        odd_line_column_count = columns - 1 if glm.length(line_length_with_offset) > glm.length(vec_right) else columns
        idx = 0
        for y in np.arange(0, rows, 1):
            is_even = y % 2 == 0
            current_line_offset = odd_line_offset if not is_even else glm.vec2(0, 0)
            start_pos = origin + right_step * 0 + down_step * y + current_line_offset
            start_idx = idx
            point = glm.vec2()
            current_columns = odd_line_column_count if not is_even else columns
            for x in np.arange(0, current_columns, 1):
                point = origin + right_step * x + down_step * y + current_line_offset
                points.append(QPointF(point.x, point.y))
                idx += 1
            end_pos = point
            end_idx = idx - 1
            lines.append({"startPos": start_pos, "startIdx": start_idx, "endPos": end_pos, "endIdx": end_idx,
                          "startEndVec": end_pos - start_pos})

        self.points = np.array(points)
        self.meta = np.array([[0, 255, 0]] * len(points))
        self.lines = np.array(lines)

        idx = 0
        origin = glm.vec2(self.points[idx])
        window_size = chip.window_size
        support_size = chip.support_size
        for y in np.arange(0, rows, 1):
            is_even = y % 2 == 0
            current_columns = odd_line_column_count if not is_even else columns
            for x in np.arange(0, current_columns, 1):
                p = glm.vec2(self.points[idx]) - origin
                p.x = p.x % (window_size.x + support_size.x)
                p.y = p.y % (window_size.y + support_size.y)
                if window_size.x <= p.x <= window_size.x + support_size.x:
                    self.meta[idx] = [255, 0, 0]
                if window_size.y <= p.y <= window_size.y + support_size.y:
                    self.meta[idx] = [255, 255, 0]
                idx += 1

    def get_bounding_points(self):
        return self.bounding_points


class GridController(ControllerBase):

    def __init__(self, generator=None):
        self.bounding_points = [glm.vec2(0, 0), glm.vec2(0, 0), glm.vec2(0, 0), glm.vec2(0, 0)]
        self.points = []
        self.meta = []
        self.lines = []
        self.tree = None

        if generator is not None:
            self.update_generator(generator)

        self.beam_size = ObservableProperty(10)
        self.beam_offset = ObservableProperty(glm.vec2(0, 0))
        self.sampleOffset = ObservableProperty(glm.vec2(0, 0))
        self.draw_original_size = ObservableProperty(False)
        self.selected_chip_name = ObservableProperty("")

    def clear(self):
        self.bounding_points = [glm.vec2(0, 0), glm.vec2(0, 0), glm.vec2(0, 0), glm.vec2(0, 0)]
        self.points = []
        self.meta = []
        self.lines = []
        self.tree = None

    def isEmpty(self):
        return self.bounding_points[0] - self.bounding_points[1] == glm.vec2(0, 0) \
                or self.bounding_points[0] - self.bounding_points[3] == glm.vec2(0, 0)

    def update_generator(self, generator):
        if generator is None:
            return
        print("building tree...", end="", flush=True)
        start = timer()
        self.points = generator.points
        self.meta = generator.meta
        self.lines = generator.lines
        self.bounding_points = generator.get_bounding_points()
        self.tree = cKDTree(np.array(generator.points))
        end = timer()
        print("done. building tree with {} points took: {}ms".format(len(self.points), int((end - start)*1000)))

    def get_point_lines(self):
        return self.lines

    def query_points(self, rect):
        if self.tree is None:
            return ([], [])
        center = rect[0] + rect[1]/2
        # enlarge by 0.1% for perfect matches (e.g. at 0/0 with no camera movement)
        radius = glm.length(rect[1] / 2) * 1.001
        idx = self.tree.query_ball_point(x=[center.x, center.y], r=radius)
        return self.points[idx], self.meta[idx]