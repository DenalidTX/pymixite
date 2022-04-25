from __future__ import annotations  # This enables us to type hint a class within its own definition.

import math
from abc import abstractmethod, ABC
from typing import Generic, Type

from src.mixite.shapes import Point
from src.mixite.hex import HexagonDataType, GridData
from src.mixite.storage import HexagonDataStorage
from src.mixite.coord import CoordinateConverter, CubeCoordinate
from src.mixite.location_metadata import SatelliteDataType


class HexagonGrid(ABC, Generic[HexagonDataType, SatelliteDataType]):

    @abstractmethod
    def get_hexagons_by_cube_range(self, from_coord: CubeCoordinate, to_coord: CubeCoordinate) -> list[HexagonDataType]:
        pass

    @abstractmethod
    def get_hexagons_by_offset_range(self, from_x: int, to_x: int, from_y: int, to_y: int) -> list[HexagonDataType]:
        pass

    @abstractmethod
    def contains_coord(self, coord: CubeCoordinate) -> bool:
        pass

    @abstractmethod
    def get_hex_by_cube_coord(self, coord: CubeCoordinate) -> HexagonDataType:
        pass

    @abstractmethod
    def get_hex_by_pixel_coord(self, coord_x: float, coord_y: float) -> HexagonDataType:
        pass

    @abstractmethod
    def get_coord_by_neighbor_index(self, coord: CubeCoordinate, index: int) -> CubeCoordinate:
        pass

    @abstractmethod
    def get_hex_by_neighbor_index(self, hexagon: HexagonDataType, index: int) -> HexagonDataType:
        pass

    @abstractmethod
    def get_neighbors_of(self, hexagon: HexagonDataType) -> list[HexagonDataType]:
        pass

    @abstractmethod
    def get_hex_by_coord_neighbor_index(self, coord: CubeCoordinate, index: int) -> HexagonDataType | None:
        pass


class HexagonGridImpl(HexagonGrid):

    NEIGHBOR_COORDS: list[list[int]] = [[1, 0], [1, -1], [0, -1], [-1, 0], [-1, 1], [0, 1]]
    NEIGHBOR_X_INDEX = 0
    NEIGHBOR_Z_INDEX = 1

    def __init__(self, grid_data: GridData, storage: HexagonDataStorage):
        self.grid_data: GridData = grid_data
        self.hexagons: list[HexagonDataType] = []
        self.storage: HexagonDataStorage = storage

    def get_hexagons_by_cube_range(self, from_coord: CubeCoordinate, to_coord: CubeCoordinate) -> list[HexagonDataType]:
        coords: list[HexagonDataType] = []

        for grid_z in range(from_coord.gridZ, to_coord.gridZ + 1):
            for grid_x in range(from_coord.gridX, to_coord.gridX + 1):
                coord: CubeCoordinate = CubeCoordinate(grid_x, grid_z)
                if self.contains_coord(coord):
                    coords.append(self.storage.get_data_for(coord))

        return coords

    def get_hexagons_by_offset_range(self, from_x: int, to_x: int, from_y: int, to_y: int) -> list[HexagonDataType]:
        coords: list[HexagonDataType] = []

        for grid_x in range(from_x, to_x + 1):
            for grid_y in range(from_y, to_y + 1):
                cube_x = CoordinateConverter.offset_coords_to_cube_x(grid_x, grid_y, self.grid_data.orientation)
                cube_z = CoordinateConverter.offset_coords_to_cube_z(grid_x, grid_y, self.grid_data.orientation)
                coord: CubeCoordinate = CubeCoordinate(cube_x, cube_z)
                if self.contains_coord(coord):
                    coords.append(self.storage.get_data_for(coord))

        return coords

    def contains_coord(self, coord: CubeCoordinate) -> bool:
        return self.storage.contains(coord)

    def get_hex_by_cube_coord(self, coord: CubeCoordinate) -> HexagonDataType:
        return self.storage.get_data_for(coord)

    def get_hex_by_pixel_coord(self, coord_x: float, coord_y: float) -> HexagonDataType | None:
        est_grid_x = math.floor(coord_x / self.grid_data.hexagonWidth)
        est_grid_y = math.floor(coord_y / self.grid_data.hexagonHeight)
        # Warning: This does not match the Kotlin code!
        grid_x = CoordinateConverter.offset_coords_to_cube_x(est_grid_x, est_grid_y, self.grid_data.orientation)
        grid_z = CoordinateConverter.offset_coords_to_cube_z(est_grid_x, est_grid_y, self.grid_data.orientation)
        hexagon = self.storage.get_data_for(self.storage.get_for_coords(grid_x, grid_z))

        if hexagon is None:
            return None

        return self.get_nearest_hex_by_pixel(hexagon, Point(coord_x, coord_y))

    def get_nearest_hex_by_pixel(self, hexagon: HexagonDataType, pixel: Point) -> HexagonDataType:
        if pixel.distance_from(hexagon.center) < self.grid_data.innerRadius:
            return hexagon

        nearest_hex = hexagon
        nearest_dist = pixel.distance_from(nearest_hex.center)

        for index in range(6):
            current_hex = self.get_hex_by_neighbor_index(hexagon, index)
            current_dist = pixel.distance_from(current_hex.center)
            if current_dist < self.grid_data.innerRadius:
                return current_hex

            if current_dist < nearest_dist:
                nearest_dist = current_dist
                nearest_hex = current_hex

        return nearest_hex

    def get_coord_by_neighbor_index(self, coord: CubeCoordinate, index: int) -> CubeCoordinate | None:
        return CubeCoordinate(coord.gridX + self.NEIGHBOR_COORDS[index][self.NEIGHBOR_X_INDEX],
                              coord.gridZ + self.NEIGHBOR_COORDS[index][self.NEIGHBOR_Z_INDEX])

    def get_hex_by_neighbor_index(self, hexagon: HexagonDataType, index: int) -> HexagonDataType:
        neighbor_coord = self.get_coord_by_neighbor_index(hexagon.get_coords(), index)
        return self.storage.get_data_for(neighbor_coord)

    def get_hex_by_coord_neighbor_index(self, coord: CubeCoordinate, index: int) -> HexagonDataType | None:
        neighbor_coord = self.get_coord_by_neighbor_index(coord, index)
        return self.storage.get_data_for(neighbor_coord)

    def get_neighbors_of(self, hexagon: HexagonDataType) -> list[HexagonDataType]:
        neighbors: list[HexagonDataType] = []
        for index in range(6):
            neighbors.append(self.get_hex_by_neighbor_index(hexagon, index))
        return neighbors

    # TODO: Verify that this worked.
    def hexagon(self, coord: CubeCoordinate) -> HexagonDataType:
        return Type[HexagonDataType](self.grid_data, coord)


