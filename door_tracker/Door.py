from typing import Tuple


class Door:

    leftUpperPoint: Tuple[int, int]
    rightUpperPoint:  Tuple[int, int]
    w: int
    h: int

    def __init__(self, x, y, w, h):
        self.leftUpperPoint = (x, y)
        self.rightUpperPoint = (x + w, y)
        self.w = w
        self.h = h
