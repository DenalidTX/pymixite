from __future__ import annotations  # This enables us to type hint a class within its own definition.

from abc import ABC, abstractmethod
from typing import Generic, Optional

from mixite.coord import CubeCoordinate
from mixite import HexagonDataType


class HexagonDataStorage(ABC, Generic[HexagonDataType]):
    """ Important: The Kotlin library associates the CubeCoordinate to a SatelliteData object.
    This library associates it with the Hexagon object instead, and the Hexagon will handle
    the SatelliteData.
    """

    @abstractmethod
    def add_coord(self, cube_coordinate: CubeCoordinate):
        pass

    @abstractmethod
    def add_coord_with_data(self, cube_coordinate: CubeCoordinate, hexagon: HexagonDataType) -> bool:
        """
        :param cube_coordinate:
        :param hexagon:
        :return: True if data was overwritten; False otherwise.
        """
        pass

    @abstractmethod
    def get_data_for(self, cube_coordinate: CubeCoordinate) -> Optional[HexagonDataType]:
        """
        :param cube_coordinate:
        :return: The HexagonDataType object associated with the given coordinate,
                 or None if no data is found.
        """
        pass

    @abstractmethod
    def contains(self, cube_coordinate: CubeCoordinate) -> bool:
        """
        :param cube_coordinate:
        :return: True if the given coordinate is already in this storage object;
                 False otherwise.
        """
        pass

    @abstractmethod
    def has_data_for(self, cube_coordinate: CubeCoordinate) -> bool:
        """
        :param cube_coordinate:
        :return: True if the given coordinate exists in this storage object and
                 the coordinate is associated with a HexagonDataType object;
                 False otherwise.
        """
        pass

    @abstractmethod
    def clear_data_for(self, cube_coordinate: CubeCoordinate) -> bool:
        """
        Delete the HexagonDataType associated with the given coordinate, if any exists.
        :param cube_coordinate:
        :return: True if data was deleted; False otherwise.
        """
        pass

    @abstractmethod
    def get_for_coords(self, cube_x: int, cube_z: int) -> CubeCoordinate | None:
        pass


class DefaultHexagonDataStorage(HexagonDataStorage, Generic[HexagonDataType]):

    def __init__(self):
        # Initially empty dictionary representing the underlying storage.
        self.cube_hex_data = dict[CubeCoordinate, Optional[HexagonDataType]]()

    def add_coord(self, cube_coordinate: CubeCoordinate):
        self.cube_hex_data[cube_coordinate] = None

    def add_coord_with_data(self, cube_coordinate: CubeCoordinate, hexagon: Optional[HexagonDataType]) -> bool:
        has_previous = cube_coordinate in self.cube_hex_data
        self.cube_hex_data[cube_coordinate] = hexagon
        return has_previous

    def get_data_for(self, cube_coordinate: CubeCoordinate) -> Optional[HexagonDataType]:
        return self.cube_hex_data.get(cube_coordinate)

    def contains(self, cube_coordinate: CubeCoordinate) -> bool:
        return cube_coordinate in self.cube_hex_data.keys()

    def has_data_for(self, cube_coordinate: CubeCoordinate) -> bool:
        return self.cube_hex_data.get(cube_coordinate) is not None

    def clear_data_for(self, cube_coordinate: CubeCoordinate) -> bool:
        return self.add_coord_with_data(cube_coordinate, None)

    def get_for_coords(self, cube_x: int, cube_z: int) -> CubeCoordinate | None:
        for coord in self.cube_hex_data.keys():
            if coord.gridX == cube_x and coord.gridZ == cube_z:
                return coord
        return None

