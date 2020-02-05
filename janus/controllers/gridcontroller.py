from timeit import default_timer as timer
import numpy as np
from scipy.spatial import cKDTree
from janus.utils.observableproperty import ObservableProperty
from janus.controllers.controllerbase import ControllerBase
import math
from PyQt5.QtGui import QVector2D
from PyQt5.QtCore import *

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
        return [ QPointF(0, 0), QPointF(0, 0), QPointF(0, 0), QPointF(0, 0) ]

'''class AABBPointGenerator(GeneratorBase):
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
        for y in np.arange(0, self.size.y() + step_y, step_y):
            startPos = QPointF(step_x, y)
            startIdx = idx
            p = QPointF()
            for x in np.arange(0, self.size.x() + step_x, step_x):
                p = QPointF(x, y) + self.pos
                points.append((p.x(), p.y()))
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
            self.pos + QPointF(self.size.x(), 0),
            self.pos + QPointF(self.size.x(), self.size.y()),
            self.pos + QPointF(0, self.size.y())
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
        columns = QPointF(vecRight) / columnSpacing
        rows = QPointF(vecDown) / lineSpacing
        rightStep = QPointF(vecRight) * columnSpacing
        downStep = QPointF(vecDown) * lineSpacing
        idx = 0
        for y in np.arange(0, rows, 1):
            startPos = origin + rightStep * 0 + downStep * y
            startIdx = idx
            p = QPointF()
            for x in np.arange(0, columns, 1):
                p = origin + rightStep * x + downStep * y
                points.append((p.x(), p.y()))
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
        return self.bounding_points'''

class ChipPointGenerator(GeneratorBase):
    def __init__(self, bounding_points, chip, full_windows):
        self.points = np.array([(0, 0)])
        self.meta = np.array([(255, 0, 0)])
        self.window_points = np.array([(0, 0)])
        self.lines = []
        self.bounding_points = bounding_points
        self.chip = chip
        self.angle = 0
        print("generating points... ", end = "", flush=True)
        start = timer()
        self.build_points(bounding_points, chip, full_windows)
        end = timer()
        print("done. generating {} points took: {}ms".format(len(self.points), int((end - start)*1000)))

    #@profile
    def build_points(self, bounding_points, chip, full_windows):
        # as floating point calculations are inherently not 100% precise it can be
        # that a rotated vector of length 500 comes out at e.g. 499.99999647, to
        # compensate this we ass a small epsilon to the length that should generally
        # not affect the whole chip size significantly but make calculations that lie
        # directly on a border (e.g. chip size is evenly divisible by hole distance)
        # more robust
        eps = 0.00001
        size_x = QVector2D(bounding_points[1] - bounding_points[0]).length() + eps
        size_y = QVector2D(bounding_points[3] - bounding_points[0]).length() + eps

        # generate point grind as numpy array of 2d tuples, e.g. [[], []...]
        # we use this as the point of truth for our grid size to calculate
        # rows/columns. numpy point generation is way faster that manual looping in python
        # for sizes > 1e6
        grid = np.mgrid[0:size_x:chip.hole_distance.x(), 0:size_y:chip.hole_distance.y()]
        if chip.odd_indentation > 0:
            #grid[0][:, 1::2] = grid[0][:-1, 1::2]
            grid[0][:, 1::2] += chip.odd_indentation

        columns = grid.shape[1]
        rows = grid.shape[2]
        points = grid.T.reshape(-1, 2)

        # translate and rotate points to match our grid transformation specified by
        # the pounding points
        vec = bounding_points[1] - bounding_points[0]
        self.angle = math.atan2(vec.y(), vec.x())
        rot = np.array([[math.cos(self.angle), -math.sin(self.angle)], [math.sin(self.angle), math.cos(self.angle)]])
        translation = bounding_points[0]
        points = points.dot(rot.T)
        points = points + (translation.x(), translation.y())
        self.points = points

        # generate meta info for every point. this info will also be returned when a point query
        # is done via the controller
        meta = np.tile({"color": [0, 255, 0], "valid": False}, [rows, columns])

        def mark_incomplete_windows(size, window_size, hole_distance, support_size, color):
            number_of_full_windows = (size + hole_distance - window_size) // (window_size + support_size) + 1
            start_point = number_of_full_windows * (window_size + support_size)
            start_row = math.floor(start_point / hole_distance)
            meta[start_row:,] = {"color": color, "valid": False}

        # mark the last unfinished windows as disabled
        if not full_windows:
            mark_incomplete_windows(size_y, chip.window_size.y(), chip.hole_distance.y(), chip.support_size.y(), [96, 0, 0])
            meta = meta.transpose()
            mark_incomplete_windows(size_x, chip.window_size.x(), chip.hole_distance.x(), chip.support_size.x(), [96, 0, 0])
            meta = meta.transpose()

        # mark all rows with support structure als invalid. we do this per row
        def mark_support_structure(size, window_size, hole_distance, support_size, color):
            if support_size == 0:
                return
            structures = math.ceil(size / (window_size + support_size))
            max_row = meta.shape[0]
            for structure_id in range(structures):
                start_pos = window_size * (structure_id + 1) + support_size * structure_id - hole_distance
                end_pos = start_pos + support_size
                start_row = math.ceil(start_pos / hole_distance)
                end_row = math.floor(end_pos / hole_distance) + 1
                end_row = min(max_row, end_row)
                for row in range(start_row, end_row):
                    meta[row,] = {"color": color, "valid": False}

        # disable the first and last of each row and column (one point border around the whole chip)
        # first and last row
        #meta[0, ] = {"color": [255, 0, 0], "valid": False}
        #meta[-1,] = {"color": [255, 0, 0], "valid": False}
        # first and last columns
        #meta[:, 0] = {"color": [255, 0, 0], "valid": False}
        #meta[:, -1] = {"color": [255, 0, 0], "valid": False}

        # we mark all support rows and then transpose and repeat the step.
        # this is faster that some python logic for the columns case as
        # it runs is numpy
        mark_support_structure(size_y, chip.window_size.y(), chip.hole_distance.y(), chip.support_size.y(), [255, 0, 0])
        meta = meta.transpose()
        mark_support_structure(size_x, chip.window_size.x(), chip.hole_distance.x(), chip.support_size.x(), [255, 0, 0])
        meta = meta.transpose()

        # calculate topleft cornerpoints of chip windows
        window_offset_x, window_offset_y = chip.hole_distance.x(), chip.hole_distance.y()
        window_tl_points = np.mgrid[-window_offset_x: size_x: (chip.window_size.x()+chip.support_size.x()),
                                -window_offset_y: size_y: (chip.window_size.y()+chip.support_size.y())]
        window_tl_points = window_tl_points.T.reshape(-1, 2)
        #window_tl_points = window_tl_points.dot(rot.T)
        #window_tl_points = window_tl_points + (translation.x(), translation.y())
        self.window_points = window_tl_points

        # make 1d array of points from the 2d array for indexing into the kdtree later on
        meta = meta.ravel()
        self.meta = meta

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
                "startEndVec": points[start] - points[end],
                "hole_count": (end - start) + 1
            }
            lines.append(entry)
        self.lines = np.array(lines)

    def get_bounding_points(self):
        return self.bounding_points


class GridController(ControllerBase):

    def __init__(self, generator=None):
        self.bounding_points = [QPointF(0, 0), QPointF(0, 0), QPointF(0, 0), QPointF(0, 0)]
        self.points = []
        self.window_points = []
        self.meta = []
        self.lines = []
        self.angle = 0
        self.tree = None
        self.chip = None

        if generator is not None:
            self.update_generator(generator)

        self.beam_size = ObservableProperty(10)
        self.beam_offset = ObservableProperty(QPointF(0, 0))
        self.beam_center_reference = ObservableProperty(QPointF(0, 0))
        self.sample_offset = ObservableProperty(QPointF(0, 0))
        self.generate_only_full_windows = ObservableProperty(False)
        self.selected_chip_name = ObservableProperty("")

    def clear(self):
        self.bounding_points = [QPointF(0, 0), QPointF(0, 0), QPointF(0, 0), QPointF(0, 0)]
        self.points = []
        self.meta = []
        self.window_points = []
        self.lines = []
        self.tree = None
        self.angle = 0

    def isEmpty(self):
        return self.bounding_points[0] - self.bounding_points[1] == QPointF(0, 0) \
                or self.bounding_points[0] - self.bounding_points[3] == QPointF(0, 0)

    def update_generator(self, generator):
        if generator is None:
            return
        print("building tree...", end="", flush=True)
        start = timer()
        self.points = generator.points
        self.meta = generator.meta
        self.window_points = generator.window_points
        self.lines = generator.lines
        self.chip = generator.chip
        self.bounding_points = generator.get_bounding_points()
        self.angle = generator.angle
        self.tree = cKDTree(np.array(generator.points))
        end = timer()
        print("done. building tree with {} points took: {}ms".format(len(self.points), int((end - start)*1000)))

    def get_beam_position(self):
        beam_pos = self.beam_center_reference.get() + self.beam_offset.get()
        return beam_pos

    def query_points(self, rect):
        if self.tree is None:
            return ([], [])
        center = rect[0] + rect[1] / 2
        # enlarge by 0.1% for perfect matches (e.g. at 0/0 with no camera movement)
        radius = QVector2D((rect[1] / 2) * 1.001).length()
        idx = self.tree.query_ball_point(x=[center.x(), center.y()], r=radius)
        return self.points[idx], self.meta[idx]