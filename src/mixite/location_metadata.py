from typing import TypeVar


class SatelliteData:
    def __init__(self):
        self.isPassable: bool = True
        self.isOpaque: bool = False
        self.movementCost: float = 1.0


# This defines a type that is any subclass of SatelliteData.
SatelliteDataType = TypeVar('SatelliteDataType', bound=SatelliteData)
