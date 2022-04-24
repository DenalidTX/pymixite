from __future__ import annotations

from math import sqrt


class Point:
    def __init__(self, x: float, y: float):
        self.coordX = x
        self.coordY = y

    def distance_from(self, other: Point) -> float:
        x_diff = self.coordX - other.coordX
        y_diff = self.coordY - other.coordY
        x_squared = x_diff * x_diff
        y_squared = y_diff * y_diff
        return sqrt(x_squared + y_squared)

    @staticmethod
    def from_position(x: float, y: float) -> Point:
        return Point(x, y)


# This class represents a literal rectangle, not a rectangular grid made of hexagons.
class Rectangle:
    def __init__(self, left: float, top: float, width: float, height: float):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

    def right(self):
        return self.left + self.width

    def bottom(self):
        return self.top + self.height

    def contains_coords(self, x: float, y: float) -> bool:
        right_edge = self.right()
        bottom_edge = self.bottom()
        return (self.left <= x <= right_edge
                and self.top <= y <= bottom_edge)

    def contains_rectangle(self, other: Rectangle) -> bool:
        """Returns true if and only if the entire other Rectangle is within the
        current object, inclusive of edges."""
        return (self.contains_coords(other.left, other.right())
                and self.contains_coords(other.right(), other.bottom()))

    def overlaps_rectangle(self, other: Rectangle) -> bool:
        """Returns true if and only if at least part of the other Rectangle is
        fully inside this one. Edge-to-edge but not inside does not count."""
        return Rectangle.__either_rectangle_overlaps(self, other)

    @staticmethod
    def __either_rectangle_overlaps(first: Rectangle, second: Rectangle) -> bool:
        """This is a static method because doing this within an instance causes
        infinite recursion."""
        return (Rectangle.__one_rectangle_overlaps(first, second)
                or Rectangle.__one_rectangle_overlaps(second, first))

    @staticmethod
    def __one_rectangle_overlaps(first: Rectangle, second: Rectangle) -> bool:
        return ((second.left < first.left < second.right()
                 or second.left < first.right() < second.right()
                 or (first.left == second.left and first.right() == second.right()))
                and (second.top < first.top < second.bottom()
                     or second.top < first.bottom() < second.bottom()
                     or (first.top == second.top and first.bottom() == second.bottom())))

    def aspect_ratio(self) -> float or None:
        if self.height == 0.0:
            return None
        else:
            return self.width / self.height

    def to_string(self):
        return "[{},{},{},{}]".format(
            self.left,
            self.top,
            self.width,
            self.height)