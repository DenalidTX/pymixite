from typing import Generic

from mixite.coord import CubeCoordinate, RotationDirection
from mixite.grid import HexagonGrid
from mixite.location_metadata import SatelliteDataType
from mixite.hex import HexagonDataType


class HexagonGridCalculator(Generic[HexagonDataType, SatelliteDataType]):

    def __init__(self, grid: HexagonGrid):
        self.grid = grid

    @staticmethod
    def calc_distance_between(first: HexagonDataType, second: HexagonDataType) -> int:
        diff_x = abs(first.get_coords().gridX - second.get_coords().gridX)
        diff_y = abs(first.get_coords().grid_y() - second.get_coords().grid_y())
        diff_z = abs(first.get_coords().gridZ - second.get_coords().gridZ)
        return max(diff_x, diff_y, diff_z)

    def calc_move_range_from(self, hexagon: HexagonDataType, distance: int) -> list[HexagonDataType]:
        in_range: list[HexagonDataType] = []
        for x in range(-distance, distance+1):
            for y in range(max(-distance, -x - distance), min(distance, -x + distance) + 1):
                z = -x - y
                coord = self.grid.get_hex_by_cube_coord(
                    CubeCoordinate(hexagon.get_coords().gridX + x, hexagon.get_coords().gridZ + z))
                if coord is not None:
                    in_range.append(coord)

        return in_range

    def rotate_hex(self, original: HexagonDataType, target: HexagonDataType, direction: RotationDirection) \
            -> HexagonDataType:
        diff_x = target.get_coords().gridX - original.get_coords().gridX
        diff_z = target.get_coords().gridZ - original.get_coords().gridZ
        diff_coord = CubeCoordinate(diff_x, diff_z)
        rotated_coord = direction.value.calculate(diff_coord)
        result_coord = CubeCoordinate(original.get_coords().gridX + rotated_coord.gridX,
                                      original.get_coords().gridZ + rotated_coord.gridZ)
        return self.grid.get_hex_by_cube_coord(result_coord)

    def calc_ring_from(self, center_hex: HexagonDataType, radius: int) -> list[HexagonDataType]:
        """As far as I can tell, it's impossible to perform this lookup with just hexagons
        because we rely on some coordinates that don't exist on the grid (particularly for
        the edges of the grid).
        """

        results: list[HexagonDataType] = []

        current_coord = CubeCoordinate(center_hex.get_coords().gridX - radius,
                                       center_hex.get_coords().gridZ + radius)
        current_hex = self.grid.get_hex_by_cube_coord(current_coord)

        for neighbor_index in range(6):
            for distance in range(radius):
                # Hex must come first because coord changes.
                current_hex = self.grid.get_hex_by_coord_neighbor_index(current_coord, neighbor_index)
                current_coord = self.grid.get_coord_by_neighbor_index(current_coord, neighbor_index)
                if current_hex is not None:
                    results.append(current_hex)

        return results

    def draw_line(self, from_hex: HexagonDataType, to_hex: HexagonDataType) -> list[HexagonDataType]:
        results: list[HexagonDataType] = []
        distance = self.calc_distance_between(from_hex, to_hex)
        if distance == 0:
            return results

        for curr_dist in range(distance + 1):
            interp_coord = self.cube_linear_interpolate(from_hex.get_coords(),
                                                        to_hex.get_coords(), 1.0 / distance * curr_dist)
            interp_hex = self.grid.get_hex_by_cube_coord(interp_coord)
            if interp_hex is not None:
                results.append(interp_hex)

        return results

    def is_visible(self, from_hex: HexagonDataType, to_hex: HexagonDataType) -> bool:
        path = self.draw_line(from_hex, to_hex)
        for path_hex in path:
            if not (path_hex == from_hex or path_hex == to_hex) and path_hex.satellite is not None:
                if path_hex.satellite.isOpaque:
                    return False
        return True

    def cube_linear_interpolate(self, from_cube: CubeCoordinate, to_cube: CubeCoordinate, sample: float) \
            -> CubeCoordinate:
        return self.round_to_cube_coord(self.linear_interpolate(from_cube.gridX, to_cube.gridX, sample),
                                        self.linear_interpolate(from_cube.grid_y(), to_cube.grid_y(), sample),
                                        self.linear_interpolate(from_cube.gridZ, to_cube.gridZ, sample))

    @staticmethod
    def linear_interpolate(from_num: float, to_num: float, sample) -> float:
        return from_num + ((to_num - from_num) * sample)

    @staticmethod
    def round_to_cube_coord(grid_x: float, grid_y: float, grid_z: float) -> CubeCoordinate:
        round_x = round(grid_x)
        round_y = round(grid_y)
        round_z = round(grid_z)

        diff_x = abs(round_x - grid_x)
        diff_y = abs(round_y - grid_y)
        diff_z = abs(round_z - grid_z)

        result_x = round_x
        result_z = round_z

        if diff_x > diff_y and diff_x > diff_z:
            result_x = -round_y - round_z
        elif diff_y <= diff_z:
            result_z = -round_x - round_y

        return CubeCoordinate(result_x, result_z)



