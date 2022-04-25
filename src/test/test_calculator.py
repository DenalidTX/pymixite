import unittest

from src.mixite.location_metadata import SatelliteData
from src.mixite.calculator import HexagonGridCalculator
from src.mixite.hex import HexagonImpl
from src.mixite.storage import DefaultHexagonDataStorage
from src.mixite.grid import GridData, HexagonGridImpl
from src.mixite.coord import CubeCoordinate, RotationDirection
from src.mixite.layout import RectangleGridLayoutStrategy, GridLayoutStrategy


class TestHexagonGridCalculator(unittest.TestCase):

    def do_init(self):
        self.layout = RectangleGridLayoutStrategy()
        self.grid = self.create_rect_grid(10, 10, CubeCoordinate.POINTY_TOP, self.layout)
        self.calculator = HexagonGridCalculator(self.grid)

    def test_calc_distance(self):
        self.do_init()
        from_hex = self.grid.get_hex_by_cube_coord(CubeCoordinate(1, 1))
        to_hex = self.grid.get_hex_by_cube_coord(CubeCoordinate(4, 5))
        self.assertEqual(7, self.calculator.calc_distance_between(from_hex, to_hex))

    def test_calc_move_range_1(self):
        self.do_init()
        hexagon = self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 7))
        expected_path: list[HexagonImpl] = [self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 6)),
                                            self.grid.get_hex_by_cube_coord(CubeCoordinate(4, 6)),
                                            self.grid.get_hex_by_cube_coord(CubeCoordinate(4, 7)),
                                            self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 8)),
                                            self.grid.get_hex_by_cube_coord(CubeCoordinate(2, 8)),
                                            self.grid.get_hex_by_cube_coord(CubeCoordinate(2, 7)),
                                            hexagon]
        self.assertEqual(sorted(expected_path), sorted(self.calculator.calc_move_range_from(hexagon, 1)))

    def test_calc_move_range_2(self):
        self.do_init()
        hexagon = self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 7))
        expected: list[HexagonImpl] = [self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 6)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(4, 6)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(4, 7)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 8)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(2, 8)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(2, 7)),

                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 5)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(4, 5)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(5, 5)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(2, 6)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(5, 6)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(1, 7)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(5, 7)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(1, 8)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(4, 8)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(1, 9)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 9)),
                                       self.grid.get_hex_by_cube_coord(CubeCoordinate(2, 9)),
                                       hexagon]
        self.assertListEqual(sorted(expected), sorted(self.calculator.calc_move_range_from(hexagon, 2)))

    def test_calc_line_many(self):
        self.do_init()
        actual = self.calculator.draw_line(self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 7)),
                                           self.grid.get_hex_by_cube_coord(CubeCoordinate(8, 1)))
        expected: list[HexagonImpl] = [
            self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 7)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(4, 6)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(5, 5)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(6, 4)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(6, 3)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(7, 2)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(8, 1))]

        self.assertListEqual(expected, actual)

    def test_calc_line_1(self):
        self.do_init()
        actual = self.calculator.draw_line(self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 7)),
                                           self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 7)))

        self.assertListEqual([], actual)

    def test_check_visibility(self):
        self.do_init()
        satellite = SatelliteData()
        satellite.isOpaque = True
        self.grid.get_hex_by_cube_coord(CubeCoordinate(2, 5)).set_satellite(satellite)
        target = self.grid.get_hex_by_cube_coord(CubeCoordinate(-3, 8))

        self.assertFalse(self.calculator.is_visible(self.grid.get_hex_by_cube_coord(CubeCoordinate(8, 1)), target))
        self.assertFalse(self.calculator.is_visible(self.grid.get_hex_by_cube_coord(CubeCoordinate(4, 4)), target))
        self.assertTrue(self.calculator.is_visible(self.grid.get_hex_by_cube_coord(CubeCoordinate(8, 3)), target))
        self.assertTrue(self.calculator.is_visible(self.grid.get_hex_by_cube_coord(CubeCoordinate(7, 1)), target))

    def test_rotate_right(self):
        self.do_init()
        start_hex = HexagonImpl(self.grid.grid_data, CubeCoordinate(3, -1))
        target_hex = HexagonImpl(self.grid.grid_data, CubeCoordinate(5, -1))
        result_hex = self.calculator.rotate_hex(start_hex, target_hex, RotationDirection.right)

        self.assertEqual(3, result_hex.get_coords().gridX)
        self.assertEqual(-4, result_hex.get_coords().grid_y())
        self.assertEqual(1, result_hex.get_coords().gridZ)

    def test_rotate_left(self):
        self.do_init()
        start_hex = HexagonImpl(self.grid.grid_data, CubeCoordinate(5, -1))
        target_hex = HexagonImpl(self.grid.grid_data, CubeCoordinate(3, -1))
        result_hex = self.calculator.rotate_hex(start_hex, target_hex, RotationDirection.left)

        self.assertEqual(3, result_hex.get_coords().gridX)
        self.assertEqual(-4, result_hex.get_coords().grid_y())
        self.assertEqual(1, result_hex.get_coords().gridZ)

    def test_calc_ring(self):
        self.do_init()
        target_hex = HexagonImpl(self.grid.grid_data, CubeCoordinate(4, 4))
        expected: list[HexagonImpl] = [
            self.grid.get_hex_by_cube_coord(CubeCoordinate(2, 7)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 7)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(4, 7)),

            self.grid.get_hex_by_cube_coord(CubeCoordinate(5, 6)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(6, 5)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(7, 4)),

            self.grid.get_hex_by_cube_coord(CubeCoordinate(7, 3)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(7, 2)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(7, 1)),

            self.grid.get_hex_by_cube_coord(CubeCoordinate(6, 1)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(5, 1)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(4, 1)),

            self.grid.get_hex_by_cube_coord(CubeCoordinate(3, 2)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(2, 3)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(1, 4)),

            self.grid.get_hex_by_cube_coord(CubeCoordinate(1, 5)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(1, 6)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(1, 7))
        ]

        self.assertListEqual(sorted(expected), sorted(self.calculator.calc_ring_from(target_hex, 3)))

    def test_calc_ring_near_edge(self):
        self.do_init()
        target_hex = HexagonImpl(self.grid.grid_data, CubeCoordinate(9, 0))
        expected: list[HexagonImpl] = [
            self.grid.get_hex_by_cube_coord(CubeCoordinate(8, 0)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(8, 1)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(9, 1))
        ]

        self.assertListEqual(sorted(expected), sorted(self.calculator.calc_ring_from(target_hex, 1)))

    def test_calc_ring_off_edge(self):
        self.do_init()
        target_hex = HexagonImpl(self.grid.grid_data, CubeCoordinate(0, -1))
        expected: list[HexagonImpl] = [
            self.grid.get_hex_by_cube_coord(CubeCoordinate(2, 0)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(1, 1)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(0, 2)),
            self.grid.get_hex_by_cube_coord(CubeCoordinate(-1, 2))
        ]

        self.assertListEqual(sorted(expected), sorted(self.calculator.calc_ring_from(target_hex, 3)))

    def test_calc_ring_radius_1(self):
        self.do_init()
        target_hex = HexagonImpl(self.grid.grid_data, CubeCoordinate(4, 4))
        self.assertEqual(6, len(self.calculator.calc_ring_from(target_hex, 1)))

    @staticmethod
    def create_rect_grid(width: int, height: int, orientation: str, layout: GridLayoutStrategy):
        coords = layout.fetch_grid_coords(width, height, orientation)
        grid_data = GridData(orientation, 10, width, height)
        grid: HexagonGridImpl = HexagonGridImpl(grid_data, DefaultHexagonDataStorage())

        for coord in coords:
            grid.storage.add_coord_with_data(coord, HexagonImpl(grid_data, coord))
        return grid


if __name__ == '__main__':
    unittest.main()
