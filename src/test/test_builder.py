import unittest

from mixite.coord import CubeCoordinate
from mixite.builder import GridControlBuilder, GridControl
from mixite.layout import GridLayoutException


class TestGridControlBuilder(unittest.TestCase):

    def test_build_valid(self):
        grid_control: GridControl = GridControlBuilder().build_rectangle(
            CubeCoordinate.POINTY_TOP,
            30,
            9,
            10)
        self.assertEqual(30, grid_control.grid_data.radius)
        self.assertEqual(9, grid_control.grid_data.gridWidth)
        self.assertEqual(10, grid_control.grid_data.gridHeight)
        self.assertEqual(CubeCoordinate.POINTY_TOP, grid_control.grid_data.orientation)
        self.assertEqual(90, len(grid_control.hex_grid.storage.cube_hex_data))

    def test_build_invalid(self):
        with self.assertRaises(GridLayoutException):
            GridControlBuilder().build_rectangle(
                CubeCoordinate.POINTY_TOP,
                30,
                0,
                10)
