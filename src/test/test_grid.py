import unittest

from mixite.coord import CubeCoordinate
from mixite.layout import RectangleGridLayoutStrategy
from mixite.shapes import Point
from mixite.location_metadata import SatelliteData
from mixite.storage import DefaultHexagonDataStorage
from mixite.grid import HexagonGridImpl
from mixite.hex import HexagonImpl, GridData


class TestGridData(unittest.TestCase):

    def test_flat(self):
        target = GridData(CubeCoordinate.FLAT_TOP, 3.0, 30, 40)

        # The non-calculated ones.
        self.assertEqual(CubeCoordinate.FLAT_TOP, target.orientation)
        self.assertEqual(3.0, target.radius)
        self.assertEqual(30, target.gridWidth)
        self.assertEqual(40, target.gridHeight)

        # The calculated ones.
        self.assertEqual(2.25, target.innerRadius)
        self.assertEqual(4.5, target.hexagonWidth)
        self.assertAlmostEqual(5.1961524227, target.hexagonHeight, 10)

    def test_pointy(self):
        target = GridData(CubeCoordinate.POINTY_TOP, 3.0, 30, 40)

        # The non-calculated ones.
        self.assertEqual(CubeCoordinate.POINTY_TOP, target.orientation)
        self.assertEqual(3.0, target.radius)
        self.assertEqual(30, target.gridWidth)
        self.assertEqual(40, target.gridHeight)

        # The calculated ones.
        self.assertAlmostEqual(2.25, target.innerRadius, 10)
        self.assertAlmostEqual(5.1961524227, target.hexagonWidth, 10)
        self.assertEqual(4.5, target.hexagonHeight)


class TestHexagonImpl(unittest.TestCase):
    EXPECTED_FLAT_POINTS = [Point(50.0, 78.0), Point(45.0, 87.0), Point(35.0, 87.0), Point(30.0, 78.0),
                            Point(35.0, 69.0), Point(45.0, 69.0)]
    EXPECTED_POINTY_POINTS = [Point(78.0, 60.0), Point(69.0, 65.0), Point(61.0, 60.0), Point(61.0, 50.0),
                              Point(69.0, 45.0), Point(78.0, 50.0)]

    def test_points_pointy(self):
        target = HexagonImpl(GridData(CubeCoordinate.POINTY_TOP, 10.0, 1, 1), CubeCoordinate(2, 3))
        for index in range(6):
            self.assertEqual(round(self.EXPECTED_POINTY_POINTS[index].coordX),
                             round(target.points[index].coordX))
            self.assertEqual(round(self.EXPECTED_POINTY_POINTS[index].coordY),
                             round(target.points[index].coordY))

    def test_points_flat(self):
        target = HexagonImpl(GridData(CubeCoordinate.FLAT_TOP, 10.0, 1, 1), CubeCoordinate(2, 3))
        for index in range(6):
            self.assertEqual(round(self.EXPECTED_FLAT_POINTS[index].coordX),
                             round(target.points[index].coordX))
            self.assertEqual(round(self.EXPECTED_FLAT_POINTS[index].coordY),
                             round(target.points[index].coordY))

    def test_get_satellite(self):
        target = HexagonImpl(GridData(CubeCoordinate.POINTY_TOP, 10.0, 1, 1), CubeCoordinate(2, 3))
        data = SatelliteData()
        target.set_satellite(data)
        self.assertEqual(data, target.satellite)
        target.clear_satellite()
        self.assertIsNone(target.satellite)

    def test_center_pointy(self):
        target = HexagonImpl(GridData(CubeCoordinate.POINTY_TOP, 10.0, 1, 1), CubeCoordinate(2, 3))
        self.assertEqual(69, round(target.center.coordX))
        self.assertEqual(55, round(target.center.coordY))

    def test_center_flat(self):
        target = HexagonImpl(GridData(CubeCoordinate.FLAT_TOP, 10.0, 1, 1), CubeCoordinate(2, 3))
        self.assertEqual(40, round(target.center.coordX))
        self.assertEqual(78, round(target.center.coordY))


class TestHexagonGridImpl(unittest.TestCase):

    def test_hexes_by_cube_range(self):
        grid = self.create_rect_grid(10, 10)

        hexes_in_range = grid.get_hexagons_by_cube_range(CubeCoordinate(2, 3), CubeCoordinate(4, 5))

        self.assertEqual(9, len(hexes_in_range))

        cubes_in_range: list[CubeCoordinate] = []
        for hexagon in hexes_in_range:
            cubes_in_range.append(hexagon.get_coords())

        for x in range(3):
            range_x = x + 2
            for z in range(3):
                range_z = z + 3
                self.assertTrue(CubeCoordinate(range_x, range_z) in cubes_in_range)

    def test_hexes_by_offset_range(self):
        grid = self.create_rect_grid(10, 10)

        hexes_in_range = grid.get_hexagons_by_offset_range(2, 4, 3, 5)

        self.assertEqual(9, len(hexes_in_range))

        cubes_in_range: list[CubeCoordinate] = []
        for hexagon in hexes_in_range:
            cubes_in_range.append(hexagon.get_coords())

        # The first expected range (z=3) uses 1-3 for x
        for x in range(3):
            range_x = x + 1
            range_z = 3
            self.assertTrue(CubeCoordinate(range_x, range_z) in cubes_in_range)

        # The second expected range (z=4 and 5) uses 0-2 for x
        for x in range(3):
            range_x = x
            for z in range(2):
                range_z = z + 4
                self.assertTrue(CubeCoordinate(range_x, range_z) in cubes_in_range)

    def test_valid_contains(self):
        grid = self.create_rect_grid(10, 10)
        self.assertTrue(grid.contains_coord(CubeCoordinate(2, 3)))
        self.assertTrue(grid.contains_coord(CubeCoordinate(1, 1)))

    def test_invalid_contains(self):
        grid = self.create_rect_grid(10, 10)
        self.assertFalse(grid.contains_coord(CubeCoordinate(-1, 0)))
        self.assertFalse(grid.contains_coord(CubeCoordinate(1, -1)))

    def test_retrieve_valid_hexagon(self):
        grid = self.create_rect_grid(10, 10)
        self.assertIsNotNone(grid.get_hex_by_cube_coord(CubeCoordinate(2, 3)))
        self.assertIsNotNone(grid.get_hex_by_cube_coord(CubeCoordinate(0, 0)))

    def test_retrieve_invalid_hexagon(self):
        grid = self.create_rect_grid(10, 10)
        self.assertIsNone(grid.get_hex_by_cube_coord(CubeCoordinate(-2, 0)))
        self.assertIsNone(grid.get_hex_by_cube_coord(CubeCoordinate(1, -1)))

    def test_retrieve_by_valid_pixel(self):
        grid = self.create_rect_grid(10, 10)

        # Case 1
        hexagon = grid.get_hex_by_pixel_coord(310.0, 255.0)
        self.assertIsNotNone(hexagon)
        self.assertEqual(3, hexagon.get_coords().gridX)
        self.assertEqual(5, hexagon.get_coords().gridZ)

        # Case 2
        hexagon = grid.get_hex_by_pixel_coord(300.0, 275.0)
        self.assertIsNotNone(hexagon)
        self.assertEqual(3, hexagon.get_coords().gridX)
        self.assertEqual(5, hexagon.get_coords().gridZ)

        # Case 3
        hexagon = grid.get_hex_by_pixel_coord(325.0, 275.0)
        self.assertIsNotNone(hexagon)
        self.assertEqual(3, hexagon.get_coords().gridX)
        self.assertEqual(5, hexagon.get_coords().gridZ)

    def test_retrieve_by_invalid_pixel(self):
        grid = self.create_rect_grid(10, 10)
        self.assertIsNone(grid.get_hex_by_pixel_coord(-50, 122))

    def test_retrieve_neighbors(self):
        grid = self.create_rect_grid(10, 10)
        hexagon = grid.get_hex_by_cube_coord(CubeCoordinate(3, 7))
        neighbors: list[HexagonImpl] = grid.get_neighbors_of(hexagon)
        self.assertTrue(HexagonImpl(grid.grid_data, CubeCoordinate(3, 6)) in neighbors)
        self.assertTrue(HexagonImpl(grid.grid_data, CubeCoordinate(4, 6)) in neighbors)
        self.assertTrue(HexagonImpl(grid.grid_data, CubeCoordinate(4, 7)) in neighbors)
        self.assertTrue(HexagonImpl(grid.grid_data, CubeCoordinate(3, 8)) in neighbors)
        self.assertTrue(HexagonImpl(grid.grid_data, CubeCoordinate(2, 8)) in neighbors)
        self.assertTrue(HexagonImpl(grid.grid_data, CubeCoordinate(2, 7)) in neighbors)

    def test_get_grid_data(self):
        grid = self.create_rect_grid(3, 7)

        self.assertEqual(3,grid.grid_data.gridWidth)
        self.assertEqual(7, grid.grid_data.gridHeight)
        self.assertEqual(30, grid.grid_data.radius)

    @staticmethod
    def create_rect_grid(width: int, height: int):
        orientation = CubeCoordinate.POINTY_TOP
        layout = RectangleGridLayoutStrategy()
        coords = layout.fetch_grid_coords(width, height, orientation)
        grid_data = GridData(orientation, 30, width, height)
        grid: HexagonGridImpl = HexagonGridImpl(grid_data, DefaultHexagonDataStorage())
        for coord in coords:
            grid.storage.add_coord_with_data(coord, HexagonImpl(grid_data, coord))
        return grid


if __name__ == '__main__':
    unittest.main()
