from ..controllers.axiscontroller import GridAxisNames, AxisController
import janus.utils.mathhelpers as mh
import numpy as np
import time
import threading
from enum import Enum

class ContinuousFocusController:

    def __init__(self, axis_controller=None):
        self.axis_controller = axis_controller
        self.stop_requested = False
        self.points = []
        self.self_last_focus_value = 0
        self.thread = threading.Thread(target=self.run, name="ContinousFocus")
        self.thread.start()

    def set_focus_points(self, points):
        """
        Points must describe a rectangle in cw order starting in the lower left corner,
        the z indicates the focused depth

        :param points:
        :return:
        """
        if len(points) == 4 and not self.validate_points(points):
            return
        self.points = points

    def is_active(self):
        return len(self.points) == 4

    def validate_points(self, points):
        return mh.get_winding_order(points) == mh.WindingOrder.Clockwise \
            and not mh.is_zero_size(points) \
            and mh.start_point_is_ll(points)

    def get_position(self):
        x = self.axis_controller.get_position(GridAxisNames.AXIS_X)
        y = self.axis_controller.get_position(GridAxisNames.AXIS_Y)
        return [x, y]

    def run(self):
        while not self.stop_requested:
            if len(self.points) != 4:
                time.sleep(0.05)
                continue

            # https://en.wikipedia.org/wiki/Bilinear_interpolation
            pos = self.get_position()
            p1 = self.points[0]
            p2 = self.points[2]

            pos[0] = max(min(pos[0], p2[0]), p1[0])
            pos[1] = max(min(pos[1], p2[1]), p1[1])

            dist = np.linalg.norm(np.array(p1) - np.array(p2))
            if dist < 0.001:
                print("invalid points zero size rect")
                time.sleep(0.05)
                continue

            q11 = self.points[0][2]
            q12 = self.points[1][2]
            q22 = self.points[2][2]
            q21 = self.points[3][2]

            val = (
                q11 * (p2[0] - pos[0]) * (p2[1] - pos[1]) +
                q21 * (pos[0] - p1[0]) * (p2[1] - pos[1]) +
                q12 * (p2[0] - pos[0]) * (pos[1] - p1[1]) +
                q22 * (pos[0] - p1[0]) * (pos[1] - p1[1])
            ) / ((p2[0] - p1[0]) * (p2[1] - p1[1]) + 0.0)
            if abs(self.self_last_focus_value - val) > 0.01:
                self.axis_controller.set_position(GridAxisNames.AXIS_Z, val)
                self.self_last_focus_value = val
            time.sleep(0.05)

    def stop_controller(self):
        self.stop_requested = True
        self.thread.join()
        pass
