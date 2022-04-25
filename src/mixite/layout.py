from abc import ABC, abstractmethod
from math import floor

from src.mixite.coord import CubeCoordinate, CoordinateConverter


class GridLayoutStrategy(ABC):

    @abstractmethod
    def fetch_grid_coords(self, width: int, height: int, orientation: str) -> list[CubeCoordinate]:
        pass

    @abstractmethod
    def check_size(self, width: int, height: int):
        pass

    @abstractmethod
    def get_name(self):
        pass


class RectangleGridLayoutStrategy(GridLayoutStrategy):

    def fetch_grid_coords(self, width: int, height: int, orientation: str) -> list[CubeCoordinate]:
        coords: list[CubeCoordinate] = []
        for y in range(height):
            for x in range(width):
                grid_x = CoordinateConverter.offset_coords_to_cube_x(x, y, orientation)
                grid_z = CoordinateConverter.offset_coords_to_cube_z(x, y, orientation)
                coords.append(CubeCoordinate(grid_x, grid_z))
        return coords

    def check_size(self, width: int, height: int):
        return width > 0 and height > 0

    def get_name(self):
        return 'RECTANGULAR'


class TriangleGridLayoutStrategy(GridLayoutStrategy):

    def fetch_grid_coords(self, width: int, height: int, orientation: str) -> list[CubeCoordinate]:
        coords: list[CubeCoordinate] = []
        # Note: Height and width must be equal for this shape to be valid.
        for z in range(height):
            end_x = height - z
            for x in range(end_x):
                coords.append(CubeCoordinate(x, z))

        return coords

    def check_size(self, width: int, height: int):
        # return width > 0 and height > 0 and width == height
        # PyCharm thinks this is simpler. I think it's obfuscated.
        return 0 < width == height > 0

    def get_name(self):
        return 'TRIANGULAR'


class TrapezoidGridLayoutStrategy(GridLayoutStrategy):

    def fetch_grid_coords(self, width: int, height: int, orientation: str) -> list[CubeCoordinate]:
        coords: list[CubeCoordinate] = []
        for z in range(height):
            for x in range(width):
                coords.append(CubeCoordinate(x, z))

        return coords

    def check_size(self, width: int, height: int):
        return width > 0 and height > 0

    def get_name(self):
        return 'TRAPEZOID'


class HexagonGridLayoutStrategy(GridLayoutStrategy):

    def fetch_grid_coords(self, width: int, height: int, orientation: str) -> list[CubeCoordinate]:
        # Don't ask me what this math means. -Denalid
        coords: list[CubeCoordinate] = []
        # Note: Dimensions are always equal.
        grid_size = height
        hex_radius = floor(grid_size / 2.0)
        start_x: int = 0
        if CubeCoordinate.FLAT_TOP == orientation:
            start_x = floor(grid_size / 2.0)
        else:
            start_x = round(grid_size / 4.0)
        min_x: int = start_x - hex_radius

        for y in range(0, grid_size):
            dist_from_mid = abs(hex_radius - y)
            for x in range(max(start_x, min_x), max(start_x, min_x) + (2 * hex_radius) - dist_from_mid + 1):
                z: int
                if CubeCoordinate.FLAT_TOP == orientation:
                    z = y - floor(grid_size / 4.0)
                else:
                    z = y
                coords.append(CubeCoordinate(x, z))
            start_x -= 1

        return coords

    def check_size(self, width: int, height: int):
        # Again, PyCharm wants to be clever. I'd rather be clear.
        return width > 0 and height > 0 \
               and width == height \
               and abs(height % 2) == 1

    def get_name(self):
        return 'HEXAGONAL'
