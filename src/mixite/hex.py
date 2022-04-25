from __future__ import annotations

import math
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar

from src.mixite.location_metadata import SatelliteDataType
from src.mixite.coord import CubeCoordinate
from src.mixite.shapes import Point, Rectangle


class Hexagon(ABC, Generic[SatelliteDataType]):

    @abstractmethod
    def set_satellite(self, data: SatelliteDataType):
        pass

    @abstractmethod
    def clear_satellite(self):
        pass

    @abstractmethod
    def get_coords(self):
        pass


# This defines a type that is any subclass of Hexagon
HexagonDataType = TypeVar('HexagonDataType', bound=Hexagon)


class GridData:

    def __init__(self, orientation: str, radius: float, grid_width: int, grid_height: int):
        self.orientation = orientation
        self.radius = radius
        self.gridWidth = grid_width
        self.gridHeight = grid_height

        # Generally I would pull out the common code, but right now there is a FIXME
        # in the Kotlin source. I'm not sure what the FIXME note means or why it's there,
        # So I'm leaving this as is until it get sorted out.
        if CubeCoordinate.FLAT_TOP == orientation:
            self.hexagonHeight = self.calc_height(radius)
            self.hexagonWidth = self.calc_width(radius)
            self.innerRadius = self.hexagonWidth / 2.0
        else:
            self.hexagonHeight = self.calc_width(radius)
            self.hexagonWidth = self.calc_height(radius)
            self.innerRadius = self.hexagonHeight / 2.0

    @staticmethod
    def calc_height(radius) -> float:
        return math.sqrt(3.0) * radius

    @staticmethod
    def calc_width(radius) -> float:
        return radius * 3.0 / 2.0


class HexagonImpl(Hexagon):

    def __init__(self, grid_data: GridData, coords: CubeCoordinate):
        self.satellite: Optional[SatelliteDataType] = None
        self.gridData = grid_data
        self.coords = coords

        self.center: Point = self.calculate_center()
        self.points: list[Point] = self.calculate_points(self.center)

        self.external_bounding_box: Rectangle = None
        self.internal_bounding_box: Rectangle = None
        self.calc_bounding_boxes()

    def set_satellite(self, data: SatelliteDataType):
        self.satellite = data

    def clear_satellite(self):
        self.satellite = None

    def calculate_center(self):
        """
                return if (HexagonOrientation.FLAT_TOP.equals(sharedData.orientation)) {
            Point.fromPosition(
                    cubeCoordinate.gridX * sharedData.hexagonWidth + sharedData.radius,
                    cubeCoordinate.gridZ * sharedData.hexagonHeight + cubeCoordinate.gridX * sharedData.hexagonHeight / 2 + sharedData.hexagonHeight / 2
            )
        } else {
            Point.fromPosition(
                    cubeCoordinate.gridX * sharedData.hexagonWidth + cubeCoordinate.gridZ * sharedData.hexagonWidth / 2 + sharedData.hexagonWidth / 2,
                    cubeCoordinate.gridZ * sharedData.hexagonHeight + sharedData.radius
            )
        }
        :return:
        """
        if CubeCoordinate.FLAT_TOP == self.gridData.orientation:
            return Point.from_position((self.coords.gridX * self.gridData.hexagonWidth) + self.gridData.radius,
                                       (self.coords.gridZ * self.gridData.hexagonHeight)
                                       + (self.coords.gridX * self.gridData.hexagonHeight / 2)
                                       + (self.gridData.hexagonHeight / 2))
        else:
            return Point.from_position((self.coords.gridX * self.gridData.hexagonWidth)
                                       + (self.coords.gridZ * self.gridData.hexagonWidth / 2)
                                       + (self.gridData.hexagonWidth / 2),
                                       (self.coords.gridZ * self.gridData.hexagonHeight) + self.gridData.radius)

    def calculate_points(self, center: Point):
        points: list[Point] = []
        for i in range(6):
            angle: float = 2.0 * math.pi / 6.0 * (i + CubeCoordinate.orientation_offsets[self.gridData.orientation])
            x = center.coordX + (self.gridData.radius * math.cos(angle))
            y = center.coordY + (self.gridData.radius * math.sin(angle))
            points.append(Point(x, y))
        return points

    def calc_bounding_boxes(self):

        x1 = self.points[3].coordX
        y1 = self.points[2].coordY
        x2 = self.points[0].coordX
        y2 = self.points[5].coordY

        center_x = self.center.coordX
        center_y = self.center.coordY

        scale = 1.25 * self.gridData.radius

        self.external_bounding_box = Rectangle(x1, y1, x2-x1, y2-y1)
        self.internal_bounding_box = Rectangle(center_x - (scale / 2.0),
                                               center_y - (scale / 2.0),
                                               1.25 * self.gridData.radius,
                                               1.25 * self.gridData.radius)

    def get_coords(self):
        return self.coords

    def __key(self):
        return self.coords

    def __lt__(self, other):
        return self.__key() < other.__key()

    def __eq__(self, o: object) -> bool:
        return self.__key() == o.__key()

    def __hash__(self) -> int:
        return super().__hash__()

    def __repr__(self) -> str:
        return "Hex at Coord: " + str(self.coords.gridX) + ", " + str(self.coords.grid_y()) + ", " + str(self.coords.gridZ)
