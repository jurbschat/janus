import threading
import time
import math
import glm
import os
import numpy as np
from scipy.interpolate import UnivariateSpline
from multiprocessing import Pool, Process, Array, Queue, Pipe, Value
import ctypes

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ..const import State
from janus.controllers.gridcontroller import BBPointGenerator, ChipPointGenerator
from janus.devices.motor import TangoMotor
from ..core import Object
from janus.utils.eventhub import global_event_hub, Event as EHEvent, EventType as EHEventType

#
# utility stuff
#

def current_milli_time():
    return int(round(time.time() * 1000))

def print_qtrans(trans):
    print([
        [trans.m11(), trans.m12(), trans.m13()],
        [trans.m21(), trans.m22(), trans.m23()],
        [trans.m31(), trans.m32(), trans.m33()]
    ])

class GridConstants:
    muToPixelRatio = 1.667 # 1mu = 1.667 pixels

    @staticmethod
    def to_pixel(value):
        return value * GridConstants.muToPixelRatio

    @staticmethod
    def to_mu(value):
        return value / GridConstants.muToPixelRatio

    '''
        general todos:
        - use transform for all draws that need them ans skil the translate shit [opt]
        - autofocus integrieren (als cpp projekt) und funktionierend machen :D
        - chip gen, color invalid points differently
        - punkte rot einfärben auf den support structures liegen
        [chip stuff]
            - move to chip corners via chip upper left offsets
            - where should poi move on the grid or on the cihp?
            - make grid place offset action fot the chip origin
        [bugs]
            - align button still works even if the action is removed from the list, where is the reference?
    '''


class GridHelpers:
    @staticmethod
    def point_in_rect(point, rect):
        left = rect.x
        top = rect.y
        right = rect.x + rect.z
        bottom = rect.y + rect.w
        isInside = point.x >= left and point.x <= right and point.y >= top and point.y <= bottom
        if isInside:
            return True
        return False


class GridWidgetAction:
    TRANSFORM = 1
    PLACE_BY_LINE = 2
    PLACE_BY_XY = 3
    PLACE_BY_FREE = 4
    SHOW_BEAMPROFILE = 5
    TAKE_SNAPSHOT = 6
    CLEAR_GRID = 7
    POI_MOVE = 8
    SET_CHIP_ORIGIN = 9
    ALIGN_TO_BEAMPROFILE = 10


class GridMovementPositions:
    UPPER_LEFT = 0
    UPPER_MIDDLE = 1
    UPPER_RIGHT = 1
    MIDDLE_LEFT = 2
    MIDDLE_MIDDLE = 3
    MIDDLE_RIGHT = 4
    LOWER_LEFT = 5
    LOWER_MIDDLE = 6
    LOWER_RIGHT = 7


class GridAxisNames:
    AXIS_X = "grid_x"
    AXIS_Y = "grid_y"
    AXIS_Z = "grid_z"


class GridPainter:
    def __init__(self):
        self.frameCount = 0
        self.frameStart = time.time()
        self.fps = 0
        # self.bgPattern = QPixmap("../../widgets/icons/grid/fillpattern.png")
        # self.prepare_arow()

    @staticmethod
    def draw_widget_border(painter):
        # brush = QBrush(self.bgPattern)
        # p = painter #QPainter()
        # p.setBrush(brush)
        painter.save()
        painter.setPen(Qt.gray)
        draw_area_rect = QRect(0, 0, painter.device().width() - 1, painter.device().height() - 1)
        # p.fillRect(drawAreaRect, brush)
        painter.drawRect(draw_area_rect)
        painter.restore()

    @staticmethod
    def draw_onaxis(transform, painter, image):
        if image is not None:
            painter.save()
            painter.setTransform(transform)
            full_rect = QRect(0, 0, image.size().width(), image.size().height())
            painter.drawImage(QRect(0, 0, int(full_rect.width()), int(full_rect.height())), image, full_rect)
            painter.restore()

    def draw_frame_info(self, transform, painter, info):
        painter.save()
        t = QTransform().translate(10, 20)
        GridPainter.draw_text_with_bg(
            t,
            painter,
            "scale: {}%".format(int(info.view_zoom_factor * 100)),
            Qt.white,
            QColor(0, 0, 0, 128)
        )
        t = QTransform().translate(painter.device().width() - 100, 20)
        GridPainter.draw_text_with_bg(
            t,
            painter,
            "frame: {:02} (fps: {:02})".format(self.frameCount, self.fps),
            Qt.white,
            QColor(0, 0, 0, 128)
        )
        self.frameCount = self.frameCount + 1
        if time.time() - self.frameStart >= 1:
            self.fps = self.frameCount
            self.frameCount = 0
            self.frameStart = time.time()
        painter.restore()

    @staticmethod
    def draw_boundingbox_with_handles(transform, painter, rect):
        p0 = rect[0]
        p1 = rect[1]
        p2 = rect[2]
        p3 = rect[3]

        # the rect is empty
        if p0 == glm.vec2(0, 0) and p2 == glm.vec2(0, 0):
            return

        painter.save()
        painter.setTransform(transform)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(Qt.red)

        painter.drawLine(QPointF(p0.x, p0.y), QPointF(p1.x, p1.y))
        painter.drawLine(QPointF(p1.x, p1.y), QPointF(p2.x, p2.y))
        painter.drawLine(QPointF(p2.x, p2.y), QPointF(p3.x, p3.y))
        painter.drawLine(QPointF(p3.x, p3.y), QPointF(p0.x, p0.y))

        painter.setPen(Qt.yellow)
        painter.setBrush(Qt.yellow)
        size = 10
        half_size = size / 2
        painter.drawEllipse(QPointF(p0[0], p0[1]), half_size, half_size)
        painter.drawEllipse(QPointF(p1[0], p1[1]), half_size, half_size)
        painter.drawEllipse(QPointF(p2[0], p2[1]), half_size, half_size)
        painter.drawEllipse(QPointF(p3[0], p3[1]), half_size, half_size)

        painter.restore()

    @staticmethod
    def draw_points(transform, painter, points, meta_info, beam_size):
        beam_size_center_offset = beam_size / 2
        painter.save()
        painter.setTransform(transform)
        painter.setBrush(Qt.transparent)
        painter.setRenderHint(QPainter.Antialiasing)
        pen_size = 1#/GridConstants.muToPixelRatio
        for point_mu, meta in zip(points, meta_info):
            color = QColor(meta["color"][0], meta["color"][1], meta["color"][2])
            painter.setPen(QPen(color, pen_size))
            painter.drawEllipse(QPointF(point_mu[0], point_mu[1]), beam_size_center_offset, beam_size_center_offset)
        painter.restore()

    @staticmethod
    def draw_beam_position(transform, image_size, painter, beam_size, beam_offset):
        painter.save()
        painter.setTransform(transform)
        painter.setRenderHint(QPainter.Antialiasing)
        beam_pos = image_size / 2 + beam_offset
        painter.setPen(QPen(Qt.yellow, 2))
        painter.drawEllipse(QPointF(beam_pos.x, beam_pos.y), beam_size / 2, beam_size / 2)
        painter.restore()

    @staticmethod
    def draw_point(transform, painter, pos, size, color, filled=False):
        size_half = size / 2
        painter.save()
        painter.setTransform(transform)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(color)
        if filled:
            painter.setBrush(color)
        painter.drawEllipse(QPointF(pos.x, pos.y), size_half, size_half)
        painter.restore()

    @staticmethod
    def draw_line(transform, painter, p0, p1, color):
        painter.save()
        painter.setTransform(transform)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(color)
        painter.drawLine(QPointF(p0.x, p0.y), QPointF(p1.x, p1.y))
        painter.restore()

    @staticmethod
    # anchor form is from upper left corner to lower right in a 9 patch style
    def draw_text_with_bg(transform, painter, text, color, bg_color, anchor=0):
        painter.save()
        painter.setTransform(transform)
        font_height = painter.fontMetrics().height()
        text_len = painter.fontMetrics().width(text)
        bg_rect = QRect(-5, -5, text_len + 10, font_height + 5)
        bg_rect.translate(0, -font_height + 5)
        anchor_offset = glm.vec2(bg_rect.width() * (anchor % 3) / 2, bg_rect.height() * int(anchor / 3) / 2)
        painter.translate(anchor_offset.x, -anchor_offset.y)
        painter.fillRect(bg_rect, bg_color)
        painter.setPen(color)
        painter.drawText(0, 0, text)

        painter.restore()


class BeamProfileCalculator:

    '''def __init__(self, np_image, image_size):
        self.np_image = np_image
        self.image_size = image_size'''

    @staticmethod
    def get_profiles(np_image, image_size):
        xProfile = np.zeros(image_size.x)
        yProfile = np.zeros(image_size.y)
        for i in range(image_size.x):
            xProfile[i] = np.sum(np_image[0:, i])
        for i in range(image_size.y):
            yProfile[i] = np.sum(np_image[i, 0:])
        return xProfile, yProfile

    @staticmethod
    def remove_noise(profile):
        noise = np.mean(profile[0:100])
        for i in range(len(profile)):
            profile[i] = max(profile[i] - noise, 0)
            #if profile[i] - noise < 0:
            #    profile[i] = 0
            #else:
            #    profile[i] = abs(profile[i] - noise)
        return profile

    #@staticmethod
    #def get_axes(np_image, image_size):
    #    xAxis = np.arange(image_size.x)
    #    for i in range(len(xAxis)):
    #        xAxis[i] = xAxis[i] * 0.8155  # for rr3
    #    yAxis = np.arange(image_size.y)
    #    for i in range(len(yAxis)):
    #        yAxis[i] = yAxis[i] * 0.8155  # for rr3
    #    return xAxis, yAxis

    @staticmethod
    def borders(profile):
        difference = max(profile) - min(profile)
        HM = difference / 2
        for i in range(len(profile)):
            if profile[i] > HM:
                below = i
                break
        for i in range(len(profile) - 1, 0, -1):
            if profile[i] > HM:
                above = i
                break
        return below, above

    #@staticmethod
    #def FWHM(arr_x, arr_y):
    #    difference = max(arr_y) - min(arr_y)
    #    HM = difference / 2
    #    pos_extremum = arr_y.argmax()
    #    nearest_above = (np.abs(arr_y[pos_extremum:-1] - HM)).argmin()
    #    nearest_below = (np.abs(arr_y[0:pos_extremum] - HM)).argmin()
    #    FWHM = (np.mean(arr_x[nearest_above + pos_extremum]) - np.mean(arr_x[nearest_below]))
    #    return FWHM

    @staticmethod
    def calculate_profile(np_image, image_size):
        #np_image = self.np_image
        #image_size = self.image_size
        profile_x, profile_y = BeamProfileCalculator.get_profiles(np_image, image_size)
        profile_x = BeamProfileCalculator.remove_noise(profile_x)
        profile_y = BeamProfileCalculator.remove_noise(profile_y)
        #axis_x, axis_y = BeamProfileCalculator.get_axes(np_image, image_size)

        below_x, above_x = BeamProfileCalculator.borders(profile_x)
        max_x = below_x + abs(above_x - below_x) / 2
        below_y, above_y = BeamProfileCalculator.borders(profile_y)
        max_y = below_y + abs(above_y - below_y) / 2

        profile_line_x = BeamProfileCalculator.remove_noise(np_image[int(max_y), 0:])
        profile_line_y = BeamProfileCalculator.remove_noise(np_image[0:, int(max_x)])

        #width_x = BeamProfileCalculator.FWHM(axis_x, profile_line_x)
        #width_y = BeamProfileCalculator.FWHM(axis_y, profile_line_y)

        return (max_x, (above_x - below_x), below_x, above_x,
                max_y, (above_y - below_y), below_y, above_y,
                profile_line_x, profile_line_y)

#
# grid classes
#

class BaseGridState:
    def __init__(self, grid_widget):
        self.grid_widget = grid_widget

    def inject_event(self, source, event):
        return False

    def do_paint(self, view_transform, painter):
        pass

    def image_changed(self, image):
        pass

    def update_priority(self):
        return 0

    def draw_priority(self):
        return 0


class MouseKeyboardState:

    def __init__(self, exclusiveCapture=False):
        self.downMap = {}
        self.keyMap = {}
        self.btnMap = {}
        self.mousePos = glm.vec2(0, 0)
        self.exclusiveCapture = exclusiveCapture

    def injectEvent(self, source, event):
        if event.type() == QEvent.MouseMove:
            oldPos = self.mousePos
            self.mousePos = glm.vec2(event.pos().x(), event.pos().y())
            if oldPos != self.mousePos:
                self.on_mouse_moved(oldPos, self.mousePos, self.mousePos - oldPos)
                return self.exclusiveCapture
        elif event.type() == QEvent.MouseButtonPress:
            self.downMap[event.button()] = self.mousePos
            self.btnMap[event.button()] = True
            self.on_mouse_down(event.button())
            return self.exclusiveCapture
        elif event.type() == QEvent.MouseButtonRelease:
            self.btnMap[event.button()] = False
            self.on_mouse_release(event.button())
            #if self.mousePos == self.get_down_pos(event.button()):
            self.on_click(event.button(), self.get_down_pos(event.button()))
            return self.exclusiveCapture
        elif event.type() == QEvent.KeyPress:
            self.keyMap[event.key()] = True
            self.on_key_down(event.key())
            return self.exclusiveCapture
        elif event.type() == QEvent.KeyRelease:
            self.keyMap[event.key()] = False
            self.on_key_up(event.key())
            return self.exclusiveCapture
        elif event.type() == QEvent.Wheel:
            self.on_mouse_wheel(event.angleDelta())
        return False

    def set_exclusive_capture(self, value):
        self.exclusiveCapture = value

    def get_exclusive_capture(self):
        return self.exclusiveCapture

    def is_btn_pressed(self, btn):
        if btn in self.btnMap:
            return self.btnMap[btn]
        return False

    def is_key_down(self, key):
        if key in self.keyMap:
            return self.keyMap[key]
        return False

    def get_down_pos(self, btn):
        if btn in self.downMap:
            return self.downMap[btn]
        return glm.vec2(0, 0)

    def on_key_down(self, key):
        pass

    def on_key_up(self, key):
        pass

    def on_click(self, btn, pos):
        pass

    def on_mouse_moved(self, oldPos, newPos, delta):
        pass

    def on_mouse_wheel(self, delta):
        pass

    def on_mouse_down(self, btn):
        pass

    def on_mouse_release(self, btn):
        pass


class GridTranslateState(BaseGridState, MouseKeyboardState):

    MOUSE_BUTTON = Qt.LeftButton

    def __init__(self, grid_widget):
        BaseGridState.__init__(self, grid_widget)
        MouseKeyboardState.__init__(self, False)
        self.translated_pos = glm.vec2(0, 0)
        self.grid_controller = grid_widget.grid_controller

    def inject_event(self, source, event):
        MouseKeyboardState.injectEvent(self, source, event)
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseButtonRelease:
            if event.button() == GridTranslateState.MOUSE_BUTTON:
                return True
        return False

    def on_mouse_moved(self, old_pos, new_pos, delta):
        if self.grid_controller.isEmpty():
            return
        if self.is_btn_pressed(GridTranslateState.MOUSE_BUTTON):
            down_pos = self.get_down_pos(GridTranslateState.MOUSE_BUTTON)
            down_pos = self.grid_widget.map_screen_to_sample(down_pos)
            current_pos = self.grid_widget.map_screen_to_sample(new_pos)
            self.translated_pos = current_pos - down_pos
            transform = QTransform()
            transform.translate(self.translated_pos.x, self.translated_pos.y)
            bb = self.grid_controller.bounding_points[0]
            self.grid_widget.state_data.transforms[GridTransform.POINT_TRANSFORM] = transform
            self.grid_widget.update()

    def on_mouse_release(self, btn):
        if self.grid_widget.grid_controller.isEmpty():
            return
        if btn == GridTranslateState.MOUSE_BUTTON and self.translated_pos != glm.vec2(0, 0):
            bounding_points = self.grid_controller.bounding_points
            rect_points = [x + self.translated_pos for x in bounding_points]
            if glm.distance(rect_points[0], rect_points[1]) <= 0.1 or glm.distance(rect_points[0], rect_points[2]) <= 0.1:
                return
            chip = self.grid_widget.chip_registry.get_chip(self.grid_controller.selected_chip_name.get())
            self.grid_controller.update_generator(ChipPointGenerator(rect_points, chip))
            self.grid_widget.state_data.transforms[GridTransform.POINT_TRANSFORM] = QTransform()
            self.translated_pos = glm.vec2(0, 0)
            self.grid_widget.update()


class FeatureSelectorState:

    def __init__(self, grid_controller):
        self.grid_controller = grid_controller

    def select_target(self, viewPos):
        sample_pos = self.grid_widget.map_screen_to_sample(viewPos)
        corners = self.grid_controller.bounding_points
        if self.grid_controller.isEmpty():
            return None
        lines = [
            (glm.vec2(corners[0]), glm.vec2(corners[1])),
            (glm.vec2(corners[1]), glm.vec2(corners[2])),
            (glm.vec2(corners[2]), glm.vec2(corners[3])),
            (glm.vec2(corners[3]), glm.vec2(corners[0]))
        ]
        # 9patch style, we use 3x3 to specify which part we selected, this is either
        # one of the 4 handles, or one of the 4 lines that mark the bounds
        for handle, idx in zip(corners, [0, 2, 8, 6]): # the 4 corners have those index from the upper left in cw order
            if self.distance_point(handle, sample_pos) <= 10:
                return idx
        for line, idx in zip(lines, [1, 5, 7, 3]): # the 4 lines have those index from the upper left in cw order
            if self.distance_line_segment(line[0], line[1], sample_pos) <= 5:
                return idx
        return None

    def distance_point(self, point, pos):
        return glm.distance(point, pos)

    def distance_line_segment(self, start, end, pos):
        d = end - start
        dr2 = d.x ** 2 + d.y ** 2
        lerp = ((pos.x - start.x) * d.x + (pos.y - start.y) * d.y) / dr2
        if lerp < 0:
            lerp = 0
        elif lerp > 1:
            lerp = 1
        xy = start + d * lerp
        xy -= pos
        dist = xy.x ** 2 + xy.y ** 2
        return math.sqrt(dist)


class GridRotateState(BaseGridState, MouseKeyboardState, FeatureSelectorState):

    MOUSE_BUTTON = Qt.LeftButton

    def __init__(self, grid_widget):
        BaseGridState.__init__(self, grid_widget)
        MouseKeyboardState.__init__(self, False)
        FeatureSelectorState.__init__(self, grid_widget.grid_controller)
        self.angle = 0
        self.cursor_9patch_mapping = {
            0: Qt.SizeBDiagCursor,
            1: Qt.SizeVerCursor,
            2: Qt.SizeFDiagCursor,
            3: Qt.SizeHorCursor,
            #4: unused,
            5: Qt.SizeHorCursor,
            6: Qt.SizeFDiagCursor,
            7: Qt.SizeVerCursor,
            8: Qt.SizeBDiagCursor,
        }
        self.active_handle = None
        self.rotation_origin_screen = glm.vec2(0, 0)
        self.rotation_origin_sample = glm.vec2(0, 0)

    def map_opposite_corner(self, corner):
        # corners: 0, 2, 6, 8
        #0 ->8, 2->6, 6->2, 8->0
        return abs(corner - 8)

    def map_corner_to_pos(self, corner):
        # corners: 0, 2, 6, 8
        # indexes: 0, 1, 2, 3
        corners = self.grid_controller.bounding_points
        lookup = { 0:0, 2:1, 6:3, 8:2 }
        if not corner in lookup:
            return None
        idx = lookup[corner]
        pos = corners[idx]
        return  pos

    def inject_event(self, source, event):
        MouseKeyboardState.injectEvent(self, source, event)
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseButtonRelease:
            handle = self.select_target(self.mousePos)
            if self.is_valid_handle(handle):
                if event.button() == GridRotateState.MOUSE_BUTTON:
                    return True
        return False

    def is_valid_handle(self, handle):
        if handle is None:
            return False
        valid = [0, 2, 6, 8]
        if handle in valid:
            return True
        return False

    def on_mouse_down(self, btn):
        if btn != GridRotateState.MOUSE_BUTTON:
            return
        handle = self.select_target(self.mousePos)
        if not self.is_valid_handle(handle):
            return
        self.active_handle = handle
        if self.grid_controller.isEmpty():
            return
        opposite_handle = self.map_opposite_corner(self.active_handle)
        self.rotation_origin_sample = self.map_corner_to_pos(opposite_handle)
        self.rotation_origin_screen = self.grid_widget.map_sample_to_screen(self.rotation_origin_sample)

    def on_mouse_moved(self, old_pos, new_pos, delta):
        handle = self.select_target(self.mousePos)
        if handle is not None:
            self.grid_widget.setCursor(self.cursor_9patch_mapping[handle])
        else:
            self.grid_widget.unsetCursor()
        if self.grid_controller.isEmpty() or not self.is_valid_handle(self.active_handle):
            return
        down_pos = self.get_down_pos(GridRotateState.MOUSE_BUTTON)
        current_pos = new_pos
        v0 = self.rotation_origin_screen - down_pos
        v1 = self.rotation_origin_screen - current_pos
        self.angle = math.atan2(v0.x * v1.y - v0.y * v1.x, v0.x * v1.x + v0.y * v1.y) * 180 / math.pi
        point_transform = QTransform()
        point_transform.translate(self.rotation_origin_sample.x, self.rotation_origin_sample.y)
        point_transform.rotate(self.angle)
        point_transform.translate(-self.rotation_origin_sample.x, -self.rotation_origin_sample.y)
        self.grid_widget.state_data.transforms[GridTransform.POINT_TRANSFORM] = point_transform
        self.grid_widget.update()

    def on_mouse_release(self, btn):
        if btn != GridRotateState.MOUSE_BUTTON:
            return
        self.active_handle = None
        if self.grid_widget.grid_controller.isEmpty() or abs(self.angle) < 0.01:
            return
        point_transform = QTransform()
        point_transform.translate(self.rotation_origin_sample.x, self.rotation_origin_sample.y)
        point_transform.rotate(self.angle)
        point_transform.translate(-self.rotation_origin_sample.x, -self.rotation_origin_sample.y)
        rect_points = [QPointF(p.x, p.y) * point_transform for p in self.grid_controller.bounding_points]
        rect_points = [glm.vec2(p.x(), p.y()) for p in rect_points]
        chip = self.grid_widget.chip_registry.get_chip(self.grid_widget.grid_controller.selected_chip_name.get())
        self.grid_controller.update_generator(ChipPointGenerator(rect_points, chip))
        self.grid_widget.state_data.transforms[GridTransform.POINT_TRANSFORM] = QTransform()
        self.angle = 0
        self.grid_widget.update()


class GridChangeDimensionState(BaseGridState, MouseKeyboardState, FeatureSelectorState):

    MOUSE_BUTTON = Qt.LeftButton

    def __init__(self, grid_widget):
        BaseGridState.__init__(self, grid_widget)
        MouseKeyboardState.__init__(self, False)
        FeatureSelectorState.__init__(self, grid_widget.grid_controller)
        self.active_handle = None
        self.mouse_offset = glm.vec2(0, 0)
        self.bounding_points = None

    def inject_event(self, source, event):
        MouseKeyboardState.injectEvent(self, source, event)
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseButtonRelease:
            handle = self.select_target(self.mousePos)
            if self.is_valid_handle(handle):
                if event.button() == GridChangeDimensionState.MOUSE_BUTTON:
                    return True
        return False

    def is_valid_handle(self, handle):
        if handle is None:
            return False
        valid = [1, 3, 5, 7]
        if handle in valid:
            return True
        return False

    def on_mouse_down(self, btn):
        if btn != GridChangeDimensionState.MOUSE_BUTTON:
            return
        handle = self.select_target(self.mousePos)
        if not self.is_valid_handle(handle):
            return
        if self.grid_widget.grid_controller.isEmpty():
            return
        self.active_handle = handle
        self.bounding_points = self.grid_controller.bounding_points.copy()

    def on_mouse_moved(self, old_pos, new_pos, delta):
        handle = self.select_target(self.mousePos)
        if self.grid_widget.grid_controller.isEmpty() or not self.is_valid_handle(self.active_handle):
            return
        down = self.grid_widget.map_screen_to_sample(self.get_down_pos(GridChangeDimensionState.MOUSE_BUTTON))
        now = self.grid_widget.map_screen_to_sample(new_pos)
        self.mouse_offset = now - down
        self.bounding_points = self.grid_controller.bounding_points.copy()
        perp_points_handle = self.get_perpendicular_indexes(self.active_handle)
        perp_points_handle_idx = self.map_handle_to_bb_indexes(perp_points_handle)
        point_offset_vec = self.bounding_points[perp_points_handle_idx[0]] - self.bounding_points[perp_points_handle_idx[1]]
        point_offset_dir = glm.normalize(point_offset_vec)
        affected_points_idx = self.map_handle_to_bb_indexes(self.active_handle)
        mouse_offset_vec = glm.dot(point_offset_dir, self.mouse_offset)
        self.bounding_points[affected_points_idx[0]] = self.bounding_points[affected_points_idx[0]] + point_offset_dir * mouse_offset_vec
        self.bounding_points[affected_points_idx[1]] = self.bounding_points[affected_points_idx[1]] + point_offset_dir * mouse_offset_vec
        self.grid_widget.update()

    def on_mouse_release(self, btn):
        if btn != GridChangeDimensionState.MOUSE_BUTTON:
            return
        if self.grid_widget.grid_controller.isEmpty() or not self.is_valid_handle(self.active_handle):
            return
        if self.bounding_points != self.grid_controller.bounding_points:
            chip = self.grid_widget.chip_registry.get_chip(self.grid_widget.grid_controller.selected_chip_name.get())
            self.grid_controller.update_generator(ChipPointGenerator(self.bounding_points, chip))
        self.bounding_points = None
        self.active_handle = None
        self.mouse_offset = glm.vec2(0, 0)
        self.grid_widget.update()

    def map_handle_to_bb_indexes(self, handle):
        lookup = {
            1: (0, 1),
            3: (3, 0),
            5: (1, 2),
            7: (2, 3)
        }
        return lookup[handle]

    def get_perpendicular_indexes(self, handle):
        lookup = {
            1: 3,
            3: 1,
            5: 7,
            7: 5
        }
        return lookup[handle]

    def do_paint(self, view_transform, painter):
        if not self.is_valid_handle(self.active_handle):
            return
        if self.bounding_points is not None:
            t = self.grid_widget.make_combined_transform()
            GridPainter.draw_boundingbox_with_handles(t, painter, self.bounding_points)


class GridMoveSampleState(BaseGridState, MouseKeyboardState):

    MOUSE_BUTTON = Qt.RightButton

    def __init__(self, grid_widget):
        BaseGridState.__init__(self, grid_widget)
        MouseKeyboardState.__init__(self, False)

    def inject_event(self, source, event):
        MouseKeyboardState.injectEvent(self, source, event)
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseButtonRelease:
            if event.button() == GridMoveSampleState.MOUSE_BUTTON:
                return True
        return False

    def on_mouse_down(self, btn):
        if btn != GridMoveSampleState.MOUSE_BUTTON:
            return
        mouse_pos = self.get_down_pos(btn)
        target = self.grid_widget.map_screen_to_sample(mouse_pos)
        self.grid_widget.move_position_to_view_center(target)

    def update_priority(self):
        return 1

    def draw_priority(self):
        return 1


class GridPlacerByChipState(BaseGridState, MouseKeyboardState):

    MOUSE_BUTTON = Qt.LeftButton

    def __init__(self, grid_widget):
        BaseGridState.__init__(self, grid_widget)
        MouseKeyboardState.__init__(self, False)
        self.points = []
        self.handleSize = 10

    def __del__(self):
        pass

    def on_click(self, btn, pos):
        if btn == GridPlacerByChipState.MOUSE_BUTTON:
            asSamplePos = self.grid_widget.map_screen_to_sample(self.mousePos)
            self.points.append(asSamplePos)
            if len(self.points) >= 2:
                if self.points[0] == self.points[1]:
                    del self.points[-1]
                    return
                self.build_new_grid()

    def on_key_down(self, key):
        if key == Qt.Key_Escape:
            if len(self.points) == 0:
                self.grid_widget.remove_states([self], GridWidgetAction.TRANSFORM)
            else:
                self.points = []

    def inject_event(self, source, event):
        MouseKeyboardState.injectEvent(self, source, event)
        if event.type() == QEvent.MouseMove:
            self.grid_widget.update()
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseButtonRelease:
            if event.button() == GridPlacerByChipState.MOUSE_BUTTON:
                return True
        return False

    def build_new_grid(self):
        chip = self.grid_widget.chip_registry.get_chip(self.grid_widget.grid_controller.selected_chip_name.get())
        bounding_points = self.build_boundingbox_from_points(self.points[0], self.points[1], chip.chip_size)
        self.grid_widget.grid_controller.update_generator(ChipPointGenerator(bounding_points, chip))
        self.points = []
        self.grid_widget.remove_states([self], GridWidgetAction.TRANSFORM)

    def build_boundingbox_from_points(self, one, two, chip_size):
        origin = one
        dir = two - origin
        vDown = glm.normalize(dir)
        vRight = glm.normalize((vDown[1], -vDown[0]))
        p0 = origin
        p1 = origin + vRight * chip_size.x
        p2 = origin + vRight * chip_size.x + vDown * chip_size.y
        p3 = origin + vDown * chip_size.y
        bounding_points = [p0, p1, p2, p3]
        return bounding_points

    def do_paint(self, view_transform, painter):
        model_view = self.grid_widget.make_combined_transform()
        if len(self.points) == 0:
            asSamplePos = self.grid_widget.map_screen_to_sample(self.mousePos)
            GridPainter.draw_point(model_view, painter, asSamplePos, self.handleSize, Qt.yellow, True)
            pass
        elif len(self.points) == 1:
            chip = self.grid_widget.chip_registry.get_chip(self.grid_widget.grid_controller.selected_chip_name.get())
            mouseInSample = self.grid_widget.map_screen_to_sample(self.mousePos)
            if glm.distance(self.points[0], mouseInSample) == 0:
                points = self.build_boundingbox_from_points(self.points[0], self.points[0] + glm.vec2(0, 1), chip.chip_size)
            else:
                points = self.build_boundingbox_from_points(self.points[0], mouseInSample, chip.chip_size)
            GridPainter.draw_boundingbox_with_handles(model_view, painter, points)

    def update_priority(self):
        return 1

    def draw_prioroty(self):
        return 1


class GridPlacerByThreePointState(BaseGridState, MouseKeyboardState):

    MOUSE_BUTTON = Qt.LeftButton

    def __init__(self, grid_widget):
        BaseGridState.__init__(self, grid_widget)
        MouseKeyboardState.__init__(self, False)
        self.points = []
        self.handleSize = 10

    def inject_event(self, source, event):
        MouseKeyboardState.injectEvent(self, source, event)
        if event.type() == QEvent.MouseMove:
            self.grid_widget.update()
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseButtonRelease:
            if event.button() == GridPlacerByThreePointState.MOUSE_BUTTON:
                return True
        return False

    def map_point_on_perp_line(self, l0, l1, p):
        vec = l1 - l0
        perp = glm.vec2(-vec.y, vec.x)
        dir = glm.normalize(perp)
        offset = p - l0
        dst = glm.dot(dir, offset)
        if dst < 0:
            dst = 0
        return dir, l0 + dir * dst

    def on_click(self, btn, pos):
        if btn == GridPlacerByThreePointState.MOUSE_BUTTON:
            click_pos = self.mousePos
            asSamplePos = self.grid_widget.map_screen_to_sample(click_pos)
            for p in self.points:
                if p == asSamplePos:
                    return
            self.add_point(asSamplePos)

    def add_point(self, p):
        if len(self.points) == 0:
            self.points.append(p)
        elif len(self.points) == 1:
            self.points.append(p)
            self.points = sorted(self.points, key=lambda p: (p.x))
        elif len(self.points) == 2:
            asSamplePos = self.grid_widget.map_screen_to_sample(self.mousePos)
            _, pol = self.map_point_on_perp_line(self.points[0], self.points[1], asSamplePos)
            self.points.append(pol)
            self.build_grid()
            self.points = []

    def on_key_down(self, key):
        if key == Qt.Key_Escape:
            if len(self.points) == 0:
                self.grid_widget.remove_states([self], GridWidgetAction.TRANSFORM)
            else:
                self.points = []

    def build_grid(self):
        chip = self.grid_widget.chip_registry.get_chip(self.grid_widget.grid_controller.selected_chip_name.get())
        p0 = self.points[0]
        p1 = self.points[1]
        v0 = self.points[1] - self.points[0]
        v1 = self.points[2] - self.points[0]
        p2 = self.points[0] + v0 + v1
        p3 = self.points[2]
        bounding_points = [p0, p1, p2, p3]
        self.grid_widget.grid_controller.update_generator(ChipPointGenerator(bounding_points, chip))
        self.points = []
        self.grid_widget.remove_states([self], GridWidgetAction.TRANSFORM)

    def do_paint(self, view_transform, painter):
        # draw line from first point to mouse
        model_view = self.grid_widget.make_combined_transform()
        if len(self.points) == 1:
            asSamplePos = self.grid_widget.map_screen_to_sample(self.mousePos)
            GridPainter.draw_line(model_view, painter, self.points[0], asSamplePos, Qt.red)
        # draw yellow circle at mouse pos as long as we have less than two points
        if len(self.points) < 2:
            # draw point at mouse pos
            asSamplePos = self.grid_widget.map_screen_to_sample(self.mousePos)
            GridPainter.draw_point(model_view, painter, asSamplePos, self.handleSize, Qt.yellow, True)
        # at two points (saved) we need to lock the third point on the perp line from our previous points
        if len(self.points) == 2:
            GridPainter.draw_line(model_view, painter, self.points[0], self.points[1], Qt.red)
            asSamplePos = self.grid_widget.map_screen_to_sample(self.mousePos)
            dir, pol = self.map_point_on_perp_line(self.points[0], self.points[1], asSamplePos)
            GridPainter.draw_line(model_view, painter, self.points[0],  + dir * 1000000, Qt.red)
            GridPainter.draw_point(model_view, painter, pol, self.handleSize, Qt.yellow, True)
        # draw all placed points ontop
        for p in self.points:
            GridPainter.draw_point(model_view, painter, p, self.handleSize, Qt.yellow, True)

    def update_priority(self):
        return 1

    def draw_prioroty(self):
        return 1


class GridShowBeamProfileState(BaseGridState, MouseKeyboardState):

    def __init__(self, grid_widget):
        BaseGridState.__init__(self, grid_widget)
        MouseKeyboardState.__init__(self, False)
        self.grid_controller = self.grid_widget.grid_controller
        self.profile = None
        self.image = None
        global_event_hub().register(EHEventType.ALIGN_BEAMOFFSET_TO_BEAMPROFILE, self.align_to_profile)

    def __del__(self):
        global_event_hub().unregister(self.align_to_profile)

    def align_to_profile(self, event):
        if self.profile:
            (max_x, width_x, below_x, above_x, max_y, width_y, below_y, above_y, profile_line_x,
             profile_line_y) = self.profile
            image_center = self.grid_widget.get_image_size() / 2
            beam_center = glm.vec2(max_x, max_y)
            offset = beam_center - image_center
            offset = GridConstants.to_mu(offset)
            self.grid_controller.beam_offset.set(offset)

    def inject_event(self, source, event):
        MouseKeyboardState.injectEvent(self, source, event)
        return False

    def image_changed(self, image):
        start = current_milli_time()
        grayscale_image = None
        if image.pixelFormat() != QPixelFormat.Grayscale:
            grayscale_image = image.convertToFormat(QImage.Format_Grayscale8)
        else:
            grayscale_image = image
        self.image = grayscale_image
        image_size = glm.ivec2(grayscale_image.width(), grayscale_image.height())
        bits = grayscale_image.bits()
        bits.setsize(int(image_size.x * image_size.y))
        np_array_image = np.frombuffer(bits, np.uint8).reshape((image_size.y, image_size.x))
        stop = current_milli_time()
        #print("converting image took: {}ms".format(stop - start))
        start = current_milli_time()
        self.profile = BeamProfileCalculator.calculate_profile(np_array_image, image_size)
        stop = current_milli_time()
        #print("calculating profile took: {}ms".format(stop - start))

    def get_translate_transform(self, pos):
        return QTransform().translate(pos.x, pos.y) * self.grid_widget.state_data.transforms[GridTransform.VIEW]

    def do_paint(self, view_transform, painter):
        if self.profile is None:
            return
        (max_x, width_x, below_x, above_x, max_y, width_y, below_y, above_y, profile_line_x,
             profile_line_y) = self.profile

        graph_height = 120
        graph_width = 120
        img_size = self.grid_widget.get_image_size() - glm.vec2(2)
        ratio = 1

        painter.save()
        painter.setTransform(view_transform)

        # draw graph backgrounds
        rect_profile_x = QRect(0, img_size.y - graph_height, img_size.x, graph_height)
        rect_profile_y = QRect(img_size.x - graph_width, 0, graph_width, img_size.y - graph_height)
        graph_bg_color = QColor(0, 0, 0, 128)
        painter.fillRect(rect_profile_x, graph_bg_color)
        painter.fillRect(rect_profile_y, graph_bg_color)

        # draw graph lines
        painter.setPen(QPen(Qt.yellow, 1, Qt.SolidLine))
        step = img_size.x / len(profile_line_x)
        for i, (p0, p1) in enumerate(zip(profile_line_x, profile_line_x[1:])):
            y0 = (img_size.y - 1) - (p0 / 255) * graph_height
            y1 = (img_size.y - 1) - (p1 / 255) * graph_height
            l0 = glm.vec2(step * i, y0)
            l1 = glm.vec2(step * (i + 1), y1)
            painter.drawLines(QLineF(l0.x, l0.y, l1.x, l1.y))
        step = img_size.y / len(profile_line_y)
        for i, (p0, p1) in enumerate(zip(profile_line_y, profile_line_y[1:])):
            x0 = (img_size.x - 1) - (p0 / 255) * graph_width
            x1 = (img_size.x - 1) - (p1 / 255) * graph_width
            l0 = glm.vec2(x0, step * i)
            l1 = glm.vec2(x1, step * (i + 1))
            painter.drawLines(QLineF(l0.x, l0.y, l1.x, l1.y))

        # draw beam borders
        rect_fwhf_x = QRect(below_x * ratio, img_size.y - graph_height, (above_x - below_x) * ratio, graph_height)
        rect_fwhf_y = QRect(img_size.x - graph_width, below_y * ratio, graph_width, (above_y - below_y) * ratio)
        beam_border_color = QColor(0, 255, 0, 128)
        painter.fillRect(rect_fwhf_x, beam_border_color)
        painter.fillRect(rect_fwhf_y, beam_border_color)

        # draw beam center lines
        painter.setPen(QPen(Qt.red, 1, Qt.DashLine))
        line_x = QLineF(max_x * ratio, 0, max_x * ratio, img_size.y)
        line_y = QLineF(0, max_y * ratio, img_size.x, max_y * ratio)
        painter.drawLines(line_x)
        painter.drawLines(line_y)

        # print beam size strings
        beam_width_text = "{:.2f} um".format(GridConstants.to_mu(width_x))
        beam_height_text = "{:.2f} um".format(GridConstants.to_mu(width_y))

        font_height = painter.fontMetrics().height()
        beam_width_text_len = painter.fontMetrics().width(beam_width_text)
        beam_height_text_len = painter.fontMetrics().width(beam_height_text)

        painter.setPen(Qt.white)
        text_offset_bw = glm.vec2(max_x * ratio - beam_width_text_len / 2,
                                  img_size.y - graph_height - painter.fontMetrics().height())
        text_offset_bh = glm.vec2(img_size.x - graph_width - beam_height_text_len - 20, max_y * ratio - 5)
        GridPainter.draw_text_with_bg(self.get_translate_transform(text_offset_bh), painter, beam_height_text,
                                      Qt.white, QColor(0, 0, 0, 128))
        GridPainter.draw_text_with_bg(self.get_translate_transform(text_offset_bw), painter, beam_width_text,
                                      Qt.white, QColor(0, 0, 0, 128))

        # draw bem center calculation mode
        fwhm_label_text = "Mode: FWHM"
        fwhm_label_text_len = painter.fontMetrics().width(fwhm_label_text)
        text_offset_fwhm = glm.vec2(img_size.x - fwhm_label_text_len - 5, img_size.y - 5)
        GridPainter.draw_text_with_bg(self.get_translate_transform(text_offset_fwhm), painter, fwhm_label_text,
                                      Qt.white, QColor(0, 0, 0, 128))

        painter.restore()


class GridTransformViewState(BaseGridState, MouseKeyboardState):

    MOVE_BUTTON = Qt.LeftButton
    RESET_BUTTON = Qt.MiddleButton

    def __init__(self, grid_widget):
        BaseGridState.__init__(self, grid_widget)
        MouseKeyboardState.__init__(self, False)
        self.view_translate = self.grid_widget.state_data.view_translate
        self.view_zoom_step = self.grid_widget.state_data.view_zoom_step
        self.view_zoom_factor = self.grid_widget.state_data.view_zoom_factor
        self.down_pos = glm.vec2(0, 0)

    def inject_event(self, source, event):
        MouseKeyboardState.injectEvent(self, source, event)
        if event.type() == QEvent.MouseButtonPress or event.type() == QEvent.MouseButtonRelease:
            return True
        if event.type() == QEvent.MouseMove and self.is_btn_pressed(GridTransformViewState.MOVE_BUTTON):
            return True
        if event.type() == QEvent.Wheel:
            return True
        return False

    def on_mouse_down(self, btn):
        if btn == GridTransformViewState.MOVE_BUTTON:
            self.down_pos = self.grid_widget.map_screen_to_view(self.get_down_pos(GridTransformViewState.MOVE_BUTTON))
        elif btn == GridTransformViewState.RESET_BUTTON:
            self.view_translate = glm.vec2(0, 0)
            self.view_zoom_factor = 1
            self.view_zoom_step = 0
            self.grid_widget.state_data.transforms[GridTransform.VIEW] = QTransform()
            self.update_state()
            self.grid_widget.update()

    def on_mouse_moved(self, old_pos, new_pos, delta):
        if self.is_btn_pressed(GridTranslateState.MOUSE_BUTTON):
            now = self.grid_widget.map_screen_to_view(new_pos)
            translate = now - self.down_pos
            self.view_translate += translate
            self.update_state()
            self.grid_widget.update()

    def on_mouse_wheel(self, delta):
        world_pre = self.mousePos / self.view_zoom_factor + self.view_translate
        self.view_zoom_step -= delta.y() / 120
        self.view_zoom_factor = math.pow(0.9, self.view_zoom_step)
        world_post = self.mousePos / self.view_zoom_factor + self.view_translate
        diff = (world_pre - world_post)
        self.view_translate = self.view_translate - diff
        self.update_state()
        self.grid_widget.update()

    def update_state(self):
        transform = QTransform()
        transform.scale(self.view_zoom_factor, self.view_zoom_factor)
        transform.translate(self.view_translate.x, self.view_translate.y)
        self.grid_widget.state_data.transforms[GridTransform.VIEW] = transform
        self.grid_widget.state_data.view_translate = self.view_translate
        self.grid_widget.state_data.view_zoom_factor = self.view_zoom_factor
        self.grid_widget.state_data.view_zoom_step = self.view_zoom_step


class PoiMovementState(BaseGridState, MouseKeyboardState):

    MOUSE_BUTTON = Qt.LeftButton

    def __init__(self, grid_widget):
        BaseGridState.__init__(self, grid_widget)
        MouseKeyboardState.__init__(self, False)
        self.active_grid_button = -1
        self.button_templates = self.build_grid_buttons(48)
        self.buttons = []
        self.grid_widget.update()

    def __del__(self):
        self.grid_widget.update()

    def build_grid_buttons(self, size):
        btns = [
            # corners
            (glm.vec4(0, 0, size, size), GridMovementPositions.UPPER_LEFT, QColor(0, 0, 255, 128), Qt.yellow),
            (glm.vec4(1, 0, size, size), GridMovementPositions.UPPER_RIGHT, QColor(0, 0, 255, 128), Qt.yellow),
            (glm.vec4(1, 1, size, size), GridMovementPositions.LOWER_RIGHT, QColor(0, 0, 255, 128), Qt.yellow),
            (glm.vec4(0, 1, size, size), GridMovementPositions.LOWER_LEFT, QColor(0, 0, 255, 128), Qt.yellow),
            # sides
            (glm.vec4(0.5, 0, size, size), GridMovementPositions.UPPER_MIDDLE, QColor(0, 0, 255, 128), Qt.yellow),
            (glm.vec4(1, 0.5, size, size), GridMovementPositions.MIDDLE_RIGHT, QColor(0, 0, 255, 128), Qt.yellow),
            (glm.vec4(0.5, 1, size, size), GridMovementPositions.LOWER_MIDDLE, QColor(0, 0, 255, 128), Qt.yellow),
            (glm.vec4(0, 0.5, size, size), GridMovementPositions.MIDDLE_LEFT, QColor(0, 0, 255, 128), Qt.yellow),
            # center
            (glm.vec4(0.5, 0.5, size, size), GridMovementPositions.MIDDLE_MIDDLE, Qt.blue, Qt.yellow),
        ]
        return btns

    def convert_buttons(self, buttons, view_size):
        converted = []
        for btn in buttons:
            normalizedPos = glm.vec2(btn[0])
            btn_size = btn[0].zw
            btn_screen_pos = normalizedPos * view_size - (normalizedPos * btn_size)
            btn_screen_rect = glm.vec4(btn_screen_pos, btn[0].zw)
            tpl = (btn[0], btn_screen_rect, btn[1], btn[2], btn[3])
            converted.append(tpl)
        return converted

    def map_norm_to_grid_bb(self, normalized_pos):
        bounding_points = self.grid_widget.grid_controller.bounding_points
        v0 = (bounding_points[1] - bounding_points[0])
        v1 = (bounding_points[3] - bounding_points[0])
        offset = v0 * normalized_pos.x + v1 * normalized_pos.y
        return bounding_points[0] + offset

    def inject_event(self, source, event):
        MouseKeyboardState.injectEvent(self, source, event)
        if self.active_grid_button != -1:
            if event.type() in (QEvent.MouseButtonPress, QEvent.MouseButtonRelease, QEvent.MouseMove):
                return True
        return False

    def find_button_for_position(self, pos):
        for i, btn in enumerate(self.buttons):
            rect = btn[1]
            if GridHelpers.point_in_rect(pos, rect):
                return i
        return -1

    def on_click(self, btn, pos):
        if btn == PoiMovementState.MOUSE_BUTTON and self.active_grid_button != -1:
            if self.grid_widget.grid_controller.isEmpty():
                print("no grid set, can not move to corners")
                return
            selected_button = self.button_templates[self.active_grid_button]
            normalized_grid_position = selected_button[0]
            center_position = self.map_norm_to_grid_bb(glm.vec2(normalized_grid_position))
            self.grid_widget.move_position_to_view_center(center_position)

    def on_mouse_moved(self, oldPos, newPos, delta):
        new_btn = self.find_button_for_position(self.mousePos)
        if new_btn != self.active_grid_button:
            self.grid_widget.unsetCursor()
            self.active_grid_button = new_btn
        self.grid_widget.update()

    def do_paint(self, view_transform, painter):
        self.buttons = self.convert_buttons(self.button_templates, self.grid_widget.get_image_size())
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setTransform(view_transform)
        for i, btn in enumerate(self.buttons):
            rect = QRect(btn[1].x, btn[1].y, btn[1].z, btn[1].w)
            if i == self.active_grid_button:
                painter.setPen(QPen(QColor(Qt.black), 3))
                painter.setBrush(QColor(Qt.green))
                painter.drawEllipse(btn[1].x, btn[1].y, btn[1].z, btn[1].w)
            else:
                painter.setPen(QPen(QColor(Qt.black), 3))
                painter.setBrush(QColor(Qt.yellow))
                painter.drawEllipse(btn[1].x, btn[1].y, btn[1].z, btn[1].w)
        painter.restore()

    def update_priority(self):
        return 2

    def draw_priority(self):
        return 2


class GridTransform:
    SAMPLE_SCALING = 0
    VIEW = 1
    POINT_TRANSFORM = 2
    SAMPLE_POSITION = 3

class GridStateData:
    def __init__(self, view_zoom_factor, view_zoom_step, view_translate, transforms):
        self.view_zoom_factor = view_zoom_factor
        self.view_zoom_step = view_zoom_step
        self.view_translate = view_translate
        self.transforms = transforms


class GridWidget(QWidget, Object, MouseKeyboardState):

    update_tick_signal = pyqtSignal()

    def __init__(self, parent=None, camera=None, grid_controller=None, axis_controller=None, chip_registry=None):
        QWidget.__init__(self, parent)
        Object.__init__(self)
        MouseKeyboardState.__init__(self, True)
        self.camera = camera
        self.axis_controller = axis_controller
        self.grid_controller = grid_controller
        self.chip_registry = chip_registry
        self.move_check_timer = QTimer()
        self.update_timer = QTimer()
        self.update_timer_start = 0
        self.image = None
        self.grid_painter = GridPainter()
        self.transforms = {
            GridTransform.SAMPLE_SCALING: QTransform().scale(GridConstants.muToPixelRatio, GridConstants.muToPixelRatio),
            GridTransform.VIEW: QTransform(),
            GridTransform.POINT_TRANSFORM: QTransform(),
            GridTransform.SAMPLE_POSITION: QTransform()
        }
        self.state_data = GridStateData(1, 2, glm.vec2(0, 0), self.transforms)
        self.activeStates = self.get_initial_states()
        self.setup_ui()
        self.connect_signals()
        self.start_update_tick()

    def __del__(self):
        self.grid_controller.selected_chip_name.unregister(self.on_chip_changed)

    def get_initial_states(self):
        return [GridTranslateState(self), GridRotateState(self), GridChangeDimensionState(self), GridMoveSampleState(self)]

    def start_update_tick(self):
        last_pos = self.query_sample_position()

        def update_done():
            elapsed = time.time() - self.update_timer_start
            return elapsed > 3

        def do_update():
            self.update()
            if update_done():
                self.update_timer.stop()

        def check_for_move():
            nonlocal last_pos
            now = self.query_sample_position()
            if last_pos != now:
                if update_done():
                    self.update_timer_start = time.time()
                    self.update_timer.timeout.connect(do_update)
                    self.update_timer.start(15)
                self.update_timer_start = time.time()
                last_pos = now

        self.move_check_timer.timeout.connect(check_for_move)
        self.move_check_timer.start(200)

    def setup_ui(self):
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(512, 512))
        self.setMouseTracking(True)
        self.installEventFilter(self)
        self.setFocusPolicy(Qt.StrongFocus)

    def connect_signals(self):
        self.camera.value_changed.connect(self.on_camera_value_changed)
        self.update_tick_signal.connect(lambda: self.update)
        self.grid_controller.selected_chip_name.register(self.on_chip_changed)
        self.grid_controller.draw_original_size.register(self.on_draw_original_size_changed)

    def eventFilter(self, source, event):
        for s in reversed(sorted(self.activeStates, key= lambda s: s.update_priority())):
            if s.inject_event(source, event):
                return True
        return MouseKeyboardState.injectEvent(self, source, event)

    def on_chip_changed(self, new_value):
        if self.grid_controller.isEmpty():
            return
        bp = self.grid_controller.bounding_points
        chip = self.chip_registry.get_chip(new_value)
        self.grid_controller.update_generator(ChipPointGenerator(bp, chip))

    def on_draw_original_size_changed(self, new_value):
        self.updateImageScaling()

    def on_camera_value_changed(self, attribute):
        if self.camera and attribute == "image":
            self.update_from_camera()

    def update_from_camera(self):
        if self.camera:
            frame = self.camera.image()
            if frame is not None:
                # we can get corrupted jpeg frames.. duno why
                new_size = glm.vec2(frame.width(), frame.height())
                if new_size.x == 0 or new_size.y == 0:
                    return
                image_size = self.get_image_size()
                self.image = frame
                for s in sorted(self.activeStates, key=lambda s: s.update_priority()):
                    s.image_changed(self.image)
        self.update()

    def set_sample_position(self, position):
        self._move_sample_position(position)

    def query_sample_position(self):
        x = self.axis_controller.get_position(GridAxisNames.AXIS_X)
        y = self.axis_controller.get_position(GridAxisNames.AXIS_Y)
        offset = glm.vec2(x, y)
        return offset

    def _move_sample_position(self, position):
        self.axis_controller.set_position(GridAxisNames.AXIS_X, position.x)
        self.axis_controller.set_position(GridAxisNames.AXIS_Y, position.y)

    def make_combined_transform(self):
        return self.transforms[GridTransform.POINT_TRANSFORM] * \
               self.transforms[GridTransform.SAMPLE_POSITION] * \
               self.transforms[GridTransform.SAMPLE_SCALING] * \
               self.transforms[GridTransform.VIEW]

    def map_screen_to_sample(self, posInView):
        t = self.make_combined_transform()
        inv, ok = t.inverted()
        if not ok:
            raise Exception("oh shit, invalid transform!")
        qp = QPointF(posInView.x, posInView.y) * inv
        return glm.vec2(qp.x(), qp.y())

    def map_sample_to_screen(self, point):
        t = self.make_combined_transform()
        qp = QPointF(point.x, point.y) * t
        return glm.vec2(qp.x(), qp.y())

    def map_screen_to_view(self, point):
        t = self.transforms[GridTransform.VIEW]
        inv, ok = t.inverted()
        if not ok:
            raise Exception("oh shit, invalid transform!")
        qp = QPointF(point.x, point.y) * inv
        return glm.vec2(qp.x(), qp.y())

    def map_view_to_screen(self, point):
        t = self.transforms[GridTransform.VIEW]
        qp = QPointF(point.x, point.y) * t
        return glm.vec2(qp.x(), qp.y())

    def move_position_to_view_center(self, position, offset=glm.vec2(0, 0)):
        target_pos = self.map_screen_to_sample(self.get_image_size() / 2)
        target_move = (target_pos + offset) - position
        new_pos = self.query_sample_position() + target_move
        self.set_sample_position(new_pos)

    def get_image_size(self):
        if self.image is not None:
            return glm.vec2(self.image.width(), self.image.height())
        return glm.vec2(0, 0)

    def on_key_down(self, key):
        if key == Qt.Key_Shift:
            self.add_state(PoiMovementState(self), GridWidgetAction.POI_MOVE)
        elif key == Qt.Key_Control:
            self.add_state(GridTransformViewState(self))

    def on_key_up(self, key):
        if key == Qt.Key_Shift:
            self.remove_states_by_type([PoiMovementState], GridWidgetAction.POI_MOVE)
        elif key == Qt.Key_Control:
            self.remove_states_by_type([GridTransformViewState])

    def paintEvent(self, event):
        print(time.time())
        if self.image is None:
            return
        painter = QPainter(self)
        sample_offset = self.query_sample_position()
        # we query in sample coordinates as the grid was created in sample coordinates
        # if the grid moves right we can see more from the left direction, therefore we invert
        # the position values
        queryRect = [
            -glm.vec2(sample_offset[0], sample_offset[1]),
            # alwasy query as much as the camera shows
            GridConstants.to_mu(self.get_image_size())
        ]

        # queried points, in sample positions
        pointsMu, metaInfo = self.grid_controller.query_points(queryRect)
        # pointsMu *= GridConstants.muToPixelRatio

        beam_size = self.grid_controller.beam_size.get()
        beam_offset = self.grid_controller.beam_offset.get()

        #sample_transform = QTransform()
        #sample_transform.translate(sample_offset.x, sample_offset.y)
        #sample_transform.scale(GridConstants.muToPixelRatio, GridConstants.muToPixelRatio)
        #self.state_data["sampleTransform"] = sample_transform
        #self.transforms[GridTransform.MODEL] = QTransform().translate(GridConstants.muToPixelRatio, GridConstants.muToPixelRatio)

        self.transforms[GridTransform.SAMPLE_POSITION] = QTransform().translate(sample_offset.x, sample_offset.y)
        view_transform = self.transforms[GridTransform.VIEW]
        sample_scale = self.transforms[GridTransform.SAMPLE_SCALING]
        model_view_projection_transform = self.make_combined_transform()

        '''view_transform = QTransform()
        view_transform.translate(500, 500)
        view_transform.rotate(45)
        view_transform.scale(0.25, 0.25)
        self.grid_painter.draw_onaxis(view_transform, painter, self.image)

        t2 = QTransform()
        t2.translate(1500, 0)
        t2.rotate(-90)
        v2 = t2 * view_transform
        self.grid_painter.draw_onaxis(v2, painter, self.image)

        t3 = QTransform()
        t3.translate(1500, 0)
        t3.rotate(-90)
        v3 = t3 * t2 * view_transform
        self.grid_painter.draw_onaxis(v3, painter, self.image)'''

        #TODO: set clipping rect to the actual image area
        #TODO: camera movement sometimes looses the initial position (seems to ber elated to other states catching the event)
        #TODO: fix move to center function, beamsize drawing
        #TODO: beamlign work even after beamligne state is "hidden"...
        #TODO: where does the grid placing lag come from?
        self.grid_painter.draw_onaxis(view_transform, painter, self.image)
        GridPainter.draw_points(model_view_projection_transform, painter, pointsMu, metaInfo, beam_size)
        GridPainter.draw_boundingbox_with_handles(model_view_projection_transform, painter, self.grid_controller.bounding_points)
        GridPainter.draw_beam_position(view_transform,
                                       self.get_image_size(),
                                       painter,
                                       beam_size * GridConstants.muToPixelRatio,
                                       beam_offset * GridConstants.muToPixelRatio)
        for s in sorted(self.activeStates, key=lambda s: s.draw_priority()):
            s.do_paint(view_transform, painter)
        self.grid_painter.draw_frame_info(view_transform, painter, self.state_data)
        GridPainter.draw_widget_border(painter)

    def add_state(self, new_state, notify=None):
        for elem in self.activeStates:
            if type(elem) == type(new_state):
                return
        self.activeStates.append(new_state)
        if notify is not None:
            global_event_hub().send(EHEvent(EHEventType.TOOLBAR_CHANGE_SELECTED, notify))

    def remove_states_by_type(self, remove_types, notify=None):
        self.activeStates = [elm for elm in self.activeStates if type(elm) not in remove_types]
        if notify is not None:
            global_event_hub().send(EHEvent(EHEventType.TOOLBAR_CHANGE_SELECTED, notify))

    def remove_states(self, remove_objects, notify=None):
        self.activeStates = [elm for elm in self.activeStates if elm not in remove_objects]
        if notify is not None:
            global_event_hub().send(EHEvent(EHEventType.TOOLBAR_CHANGE_SELECTED, notify))

    def change_grid_state(self, grid_action, data = None):
        options = {
            GridWidgetAction.TRANSFORM: self.handle_action_transform,
            GridWidgetAction.PLACE_BY_LINE: self.handle_place_by_line,
            GridWidgetAction.PLACE_BY_XY: self.handle_place_by_xy,
            GridWidgetAction.SHOW_BEAMPROFILE: self.handle_show_beamprofile,
            GridWidgetAction.TAKE_SNAPSHOT: self.handle_action_snapshot,
            GridWidgetAction.CLEAR_GRID: self.handle_action_clear,
            GridWidgetAction.POI_MOVE: self.handle_poi_move,
            GridWidgetAction.SET_CHIP_ORIGIN: self.handle_set_chip_origin,
        }
        options[grid_action](data)

    def handle_set_chip_origin(self, checked):
        print("i am missing, build me!")
        # todo: create action that takes the current mouse pos and sets it as chip origin
        # todo: also update the current chip with the new origin

    def handle_align_beamprofile(self, data):
        pass

    def handle_action_clear(self, checked):
        self.grid_controller.clear()

    def handle_action_transform(self, checked):
        self.reset_states()

    def handle_place_by_line(self, checked):
        self.add_state(GridPlacerByChipState(self))

    def handle_place_by_xy(self, checked):
        self.add_state(GridPlacerByThreePointState(self))

    def handle_action_snapshot(self, checked):
        name = QFileDialog.getSaveFileName(parent=self, caption='Save File', directory="snapshot.png",
                                           filter="Images (*.png *.)")
        if name[0] is None or name[0] == "":
            return
        if self.image:
            self.image.save(name[0])
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Unable to save image as no image was received yet")
            # msg.setInformativeText("This is additional information")
            msg.setWindowTitle("Unable to take snapshot")
            msg.setStandardButtons(QMessageBox.Ok)
            retval = msg.exec_()

    def handle_show_beamprofile(self, checked):
        if checked:
            self.add_state(GridShowBeamProfileState(self))
        else:
            self.remove_states_by_type([GridShowBeamProfileState])

    def handle_poi_move(self, checked):
        if checked:
            self.add_state(PoiMovementState(self))
        else:
            self.remove_states_by_type([PoiMovementState])

    def reset_states(self):
        remove_types = [GridPlacerByChipState, GridPlacerByThreePointState]
        self.activeStates = [elm for elm in self.activeStates if type(elm) not in remove_types]

