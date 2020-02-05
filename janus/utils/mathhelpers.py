from enum import Enum
import numpy as np

class WindingOrder(Enum):
    Clockwise = 0
    CounterClockwise = 1

def get_winding_order(points):
    signed_area = 0
    idx = 0
    for point, next in zip(points, points[1:]):
        x1 = point[0]
        y1 = point[1]
        if idx == len(points) -1:
            x2 = points[0][0]
            y2 = points[0][1]
        else:
            x2 = next[0]
            y2 = next[1]
        signed_area += (x1 * y2 - x2 * y1)
    return WindingOrder.Clockwise if (signed_area / 2 < 0) else WindingOrder.CounterClockwise

def is_zero_size(points):
    p = np.array(points)
    diagonal = p[2] - p[0]
    return abs(diagonal[0]) < 0.001 or abs(diagonal[1]) < 0.001

def start_point_is_ll(points):
    p = np.array(points)
    diagonal = p[2] - p[0]
    return diagonal[0] > 0 and diagonal[1] > 0