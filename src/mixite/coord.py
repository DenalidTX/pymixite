from __future__ import annotations

import math
from abc import ABC, abstractmethod
from enum import Enum


class CubeCoordinate:

    POINTY_TOP = 'POINTY_TOP'
    FLAT_TOP = 'FLAT_TOP'

    # In the Kotlin library, this is HexagonOrientation.
    orientation_offsets: dict[str, float] = {POINTY_TOP: 0.5, FLAT_TOP: 0.0}

    def __init__(self, x: int, z: int):
        self.gridX = x
        self.gridZ = z

    def grid_y(self) -> int:
        return -(self.gridX + self.gridZ)

    def to_axial_key(self) -> str:
        return str(self.gridX) + "," + str(self.gridZ)

    @staticmethod
    def from_axial_key(axial_key: str) -> CubeCoordinate:
        key_parts = axial_key.split(",")
        return CubeCoordinate(int(key_parts[0]), int(key_parts[1]))

    def __key(self):
        return self.gridX, self.gridZ

    def __lt__(self, o: object) -> bool:
        return self.__key() < o.__key()

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        return self.__key() == other.__key()

    def __repr__(self) -> str:
        return "Coord: " + str(self.gridX) + ", " + str(self.grid_y()) + ", " + str(self.gridZ)


class RotationBase(ABC):

    @abstractmethod
    def calculate(self):
        pass


class RotationDirection(Enum):
    right = type('RightRotation', (RotationBase, object),
                 {"calculate": lambda coord: CubeCoordinate(-coord.gridZ, -coord.grid_y())})
    left = type('LeftRotation', (RotationBase, object),
                {"calculate": lambda coord: CubeCoordinate(-coord.grid_y(), -coord.gridX)})


class CoordinateConverter:

    @staticmethod
    def offset_coords_to_cube_x(offset_x: int, offset_y: int, orientation: str) -> int:
        if CubeCoordinate.FLAT_TOP == orientation:
            return offset_x
        else:
            return math.ceil(offset_x - (offset_y / 2))

    @staticmethod
    def offset_coords_to_cube_z(offset_x: int, offset_y: int, orientation: str):
        """
        Someone please explain this to me. -Denalid

        x_a = col_o
        y_a = row_o - ((col_o - (col_o & 1)) / 2)

        x_c = x_a
        y_c = y_a
        z_c = -x_c - y_c
            = -col_o - (row_o - ((col_o - (col_o & 1)) / 2))
            = -col_o - row_o + ((col_o - (col_o & 1)) / 2)

        :param offset_x:
        :param offset_y:
        :param orientation:
        :return:
        """

        if CubeCoordinate.FLAT_TOP == orientation:
            return math.ceil(offset_y - (offset_x / 2))
        else:
            return offset_y

    @staticmethod
    def cube_coords_to_offset_row(coord: CubeCoordinate, orientation: str):
        if CubeCoordinate.FLAT_TOP == orientation:
            return coord.gridZ + ((coord.gridX - (coord.gridX & 1)) / 2)
        else:
            return coord.gridZ

    @staticmethod
    def cube_coords_to_offset_column(coord: CubeCoordinate, orientation: str):
        if CubeCoordinate.FLAT_TOP == orientation:
            return coord.gridX
        else:
            return coord.gridX + ((coord.gridZ - (coord.gridZ & 1)) / 2)
