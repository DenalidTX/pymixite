import unittest

from src.mixite.coord import CubeCoordinate, CoordinateConverter, RotationDirection


def create_incomplete_key():
    axial_key = "438"
    return CubeCoordinate.from_axial_key(axial_key)


def create_malformed_key():
    axial_key = "1,a"
    return CubeCoordinate.from_axial_key(axial_key)


class TestCubeCoordinate(unittest.TestCase):

    def test_store_coords(self):
        x = 15
        z = 29
        coord = CubeCoordinate(x, z)
        self.assertEqual(x, coord.gridX)
        self.assertEqual(z, coord.gridZ)

    def test_equal_self(self):
        coord = CubeCoordinate(97, 34)
        self.assertEqual(coord, coord)

    def test_create_axial(self):
        axial_key = CubeCoordinate(7, 91).to_axial_key()
        self.assertEqual("7,91", axial_key)

    def test_read_axial(self):
        axial_key = "4,38"
        coord = CubeCoordinate.from_axial_key(axial_key)
        self.assertEqual(4, coord.gridX)
        self.assertEqual(38, coord.gridZ)

    def test_err_on_incomplete_key(self):
        self.assertRaises(IndexError, create_incomplete_key)

    def test_err_on_malformed_key(self):
        self.assertRaises(ValueError, create_malformed_key)


class TestRotationDirection(unittest.TestCase):

    def test_rotate_right(self):
        """
        This only calculates the coordinate offsets, not the full rotation.
        For that, see HexGridCalculator.
        """
        original_coord = CubeCoordinate(3, -1)
        result = RotationDirection['right'].value.calculate(original_coord)
        self.assertEqual(1, result.gridX)
        self.assertEqual(-3, result.grid_y())
        self.assertEqual(2, result.gridZ)

    def test_rotate_left(self):
        """
        This only calculates the coordinate offsets, not the full rotation.
        For that, see HexGridCalculator.
        """
        original_coord = CubeCoordinate(5, -1)
        result = RotationDirection['left'].value.calculate(original_coord)
        self.assertEqual(4, result.gridX)
        self.assertEqual(1, result.grid_y())
        self.assertEqual(-5, result.gridZ)


class TestCoordinateConverter(unittest.TestCase):

    testCubes: list[CubeCoordinate] = [CubeCoordinate(-1, -2), CubeCoordinate(2, -3), CubeCoordinate(7, 8)]
    expectedOffsetColFlat = [-1, 2, 7]
    expectedOffsetRowFlat = [-3, -2, 11]
    expectedOffsetColPointy = [-2, 0, 11]
    expectedOffsetRowPointy = [-2, -3, 8]

    def test_offset_to_axial_x_pointy(self):
        result = CoordinateConverter.offset_coords_to_cube_x(3, 4, CubeCoordinate.POINTY_TOP)
        self.assertEqual(1, result)

    def test_offset_to_axial_x_flat(self):
        result = CoordinateConverter.offset_coords_to_cube_x(3, 4, CubeCoordinate.FLAT_TOP)
        self.assertEqual(3, result)

    def test_offset_to_axial_z_pointy(self):
        result = CoordinateConverter.offset_coords_to_cube_z(3, 4, CubeCoordinate.POINTY_TOP)
        self.assertEqual(4, result)

    def test_offset_to_axial_z_flat(self):
        result = CoordinateConverter.offset_coords_to_cube_z(3, 4, CubeCoordinate.FLAT_TOP)
        self.assertEqual(3, result)

    def test_cube_to_offset_row_flat(self):
        for index in range(len(self.testCubes)):
            result = CoordinateConverter.cube_coords_to_offset_row(self.testCubes[index], CubeCoordinate.FLAT_TOP)
            self.assertEqual(self.expectedOffsetRowFlat[index], result)

    def test_cube_to_offset_column_flat(self):
        for index in range(len(self.testCubes)):
            result = CoordinateConverter.cube_coords_to_offset_column(self.testCubes[index], CubeCoordinate.FLAT_TOP)
            self.assertEqual(self.expectedOffsetColFlat[index], result)

    def test_cube_to_offset_row_pointy(self):
        for index in range(len(self.testCubes)):
            result = CoordinateConverter.cube_coords_to_offset_row(self.testCubes[index], CubeCoordinate.POINTY_TOP)
            self.assertEqual(self.expectedOffsetRowPointy[index], result)

    def test_cube_to_offset_column_pointy(self):
        for index in range(len(self.testCubes)):
            result = CoordinateConverter.cube_coords_to_offset_column(self.testCubes[index], CubeCoordinate.POINTY_TOP)
            self.assertEqual(self.expectedOffsetColPointy[index], result)


if __name__ == '__main__':
    unittest.main()
