import unittest

from mixite.coord import CubeCoordinate
from mixite.layout import RectangleGridLayoutStrategy, TriangleGridLayoutStrategy, TrapezoidGridLayoutStrategy, \
    HexagonGridLayoutStrategy, GridLayoutException


def test_invalid_params(caller, strategy, invalid_pairs):
    for width, height in invalid_pairs:
        with caller.assertRaises(GridLayoutException):
            strategy.check_size(width, height)


class TestRectangleLayout(unittest.TestCase):

    def test_pointy(self):
        strategy = RectangleGridLayoutStrategy()
        coords = strategy.fetch_grid_coords(3, 3, CubeCoordinate.POINTY_TOP)

        self.assertTrue(CubeCoordinate(0, 0) in coords)
        self.assertTrue(CubeCoordinate(1, 0) in coords)
        self.assertTrue(CubeCoordinate(2, 0) in coords)
        self.assertTrue(CubeCoordinate(0, 1) in coords)
        self.assertTrue(CubeCoordinate(1, 1) in coords)
        self.assertTrue(CubeCoordinate(2, 1) in coords)
        self.assertTrue(CubeCoordinate(-1, 2) in coords)
        self.assertTrue(CubeCoordinate(0, 2) in coords)
        self.assertTrue(CubeCoordinate(1, 2) in coords)

        self.assertTrue(CubeCoordinate(-1, 0) not in coords)
        self.assertTrue(CubeCoordinate(0, -1) not in coords)
        self.assertTrue(CubeCoordinate(1, -1) not in coords)
        self.assertTrue(CubeCoordinate(2, -1) not in coords)
        self.assertTrue(CubeCoordinate(3, -1) not in coords)
        self.assertTrue(CubeCoordinate(3, 0) not in coords)
        self.assertTrue(CubeCoordinate(3, 1) not in coords)
        self.assertTrue(CubeCoordinate(2, 2) not in coords)
        self.assertTrue(CubeCoordinate(1, 3) not in coords)
        self.assertTrue(CubeCoordinate(0, 3) not in coords)
        self.assertTrue(CubeCoordinate(-1, 3) not in coords)
        self.assertTrue(CubeCoordinate(-2, 3) not in coords)
        self.assertTrue(CubeCoordinate(-2, 2) not in coords)
        self.assertTrue(CubeCoordinate(-1, 1) not in coords)

    def test_flat(self):
        strategy = RectangleGridLayoutStrategy()
        coords = strategy.fetch_grid_coords(3, 3, CubeCoordinate.FLAT_TOP)

        self.assertTrue(CubeCoordinate(0, 0) in coords)
        self.assertTrue(CubeCoordinate(1, 0) in coords)
        self.assertTrue(CubeCoordinate(2, -1) in coords)
        self.assertTrue(CubeCoordinate(0, 1) in coords)
        self.assertTrue(CubeCoordinate(1, 1) in coords)
        self.assertTrue(CubeCoordinate(2, 0) in coords)
        self.assertTrue(CubeCoordinate(2, 1) in coords)
        self.assertTrue(CubeCoordinate(0, 2) in coords)
        self.assertTrue(CubeCoordinate(1, 2) in coords)

        self.assertTrue(CubeCoordinate(-1, 0) not in coords)
        self.assertTrue(CubeCoordinate(0, -1) not in coords)
        self.assertTrue(CubeCoordinate(1, -1) not in coords)
        self.assertTrue(CubeCoordinate(2, -2) not in coords)
        self.assertTrue(CubeCoordinate(3, -1) not in coords)
        self.assertTrue(CubeCoordinate(3, 0) not in coords)
        self.assertTrue(CubeCoordinate(3, 1) not in coords)
        self.assertTrue(CubeCoordinate(2, 2) not in coords)
        self.assertTrue(CubeCoordinate(1, 3) not in coords)
        self.assertTrue(CubeCoordinate(0, 3) not in coords)
        self.assertTrue(CubeCoordinate(-1, 3) not in coords)
        self.assertTrue(CubeCoordinate(-2, 3) not in coords)
        self.assertTrue(CubeCoordinate(-2, 2) not in coords)
        self.assertTrue(CubeCoordinate(-1, 1) not in coords)

    def test_invalid_params(self):
        strategy = RectangleGridLayoutStrategy()

        invalid_pairs = [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, -1],
            [-1, 1]
        ]

        test_invalid_params(self, strategy, invalid_pairs)

    def test_valid_params(self):
        strategy = RectangleGridLayoutStrategy()
        self.assertIsNone(strategy.check_size(1, 1))
        self.assertIsNone(strategy.check_size(1, 100))
        self.assertIsNone(strategy.check_size(100, 1))


def contains_all(list1, list2) -> bool:
    return all(elem in list1 for elem in list2)


def contains_none(list1, list2) -> bool:
    return not any(elem in list1 for elem in list2)


class TestTriangleGridLayoutStrategy(unittest.TestCase):

    validCoords: list[CubeCoordinate] = [
        CubeCoordinate(0, 0),
        CubeCoordinate(1, 0),
        CubeCoordinate(2, 0),
        CubeCoordinate(0, 1),
        CubeCoordinate(1, 1),
        CubeCoordinate(0, 2)
    ]

    invalidCoords: list[CubeCoordinate] = [
        CubeCoordinate(-1, 0),
        CubeCoordinate(0, -1),
        CubeCoordinate(1, -1),
        CubeCoordinate(2, -1),
        CubeCoordinate(3, -1),
        CubeCoordinate(3, 0),
        CubeCoordinate(2, 1),
        CubeCoordinate(1, 2),
        CubeCoordinate(0, 3),
        CubeCoordinate(-1, 3),
        CubeCoordinate(-1, 2),
        CubeCoordinate(-1, 1)
    ]

    def test_pointy(self):
        strategy = TriangleGridLayoutStrategy()
        coords = strategy.fetch_grid_coords(3, 3, CubeCoordinate.POINTY_TOP)
        self.assertTrue(contains_all(coords, self.validCoords))
        self.assertTrue(contains_none(coords, self.invalidCoords))

    def test_flat(self):
        strategy = TriangleGridLayoutStrategy()
        coords = strategy.fetch_grid_coords(3, 3, CubeCoordinate.FLAT_TOP)
        self.assertTrue(contains_all(coords, self.validCoords))
        self.assertTrue(contains_none(coords, self.invalidCoords))

    def test_check_size(self):
        strategy = TriangleGridLayoutStrategy()
        self.assertIsNone(strategy.check_size(1, 1))

        invalid_pairs = [
            [0, 0],
            [1, 2],
            [-1, -1]
        ]

        test_invalid_params(self, strategy, invalid_pairs)


class TestTrapezoidGridLayoutStrategy(unittest.TestCase):

    validCoords: list[CubeCoordinate] = [
        CubeCoordinate(0, 0),
        CubeCoordinate(1, 0),
        CubeCoordinate(2, 0),
        CubeCoordinate(2, 1),
        CubeCoordinate(2, 2),
        CubeCoordinate(1, 2),
        CubeCoordinate(0, 2),
        CubeCoordinate(0, 1)
    ]

    invalidCoords: list[CubeCoordinate] = [
        CubeCoordinate(-1, 0),
        CubeCoordinate(0, -1),
        CubeCoordinate(1, -1),
        CubeCoordinate(2, -1),
        CubeCoordinate(3, -1),
        CubeCoordinate(3, 0),
        CubeCoordinate(3, 1),
        CubeCoordinate(3, 2),
        CubeCoordinate(2, 3),
        CubeCoordinate(1, 3),
        CubeCoordinate(0, 3),
        CubeCoordinate(-1, 2),
        CubeCoordinate(-1, 1)
    ]

    def test_pointy(self):
        strategy = TrapezoidGridLayoutStrategy()
        coords = strategy.fetch_grid_coords(3, 3, CubeCoordinate.POINTY_TOP)
        self.assertTrue(contains_all(coords, self.validCoords))
        self.assertTrue(contains_none(coords, self.invalidCoords))

    def test_flat(self):
        strategy = TrapezoidGridLayoutStrategy()
        coords = strategy.fetch_grid_coords(3, 3, CubeCoordinate.FLAT_TOP)
        self.assertTrue(contains_all(coords, self.validCoords))
        self.assertTrue(contains_none(coords, self.invalidCoords))

    def test_check_size(self):
        strategy = TrapezoidGridLayoutStrategy()
        self.assertIsNone(strategy.check_size(2, 2))

        invalid_pairs = [
            [0, 0],
            [-1, -1],
        ]

        test_invalid_params(self, strategy, invalid_pairs)


class TestHexagonGridLayoutStrategy(unittest.TestCase):

    validCoords5Flat: list[CubeCoordinate] = [
        CubeCoordinate(2, -1),
        CubeCoordinate(3, -1),
        CubeCoordinate(4, -1),
        CubeCoordinate(4, 0),
        CubeCoordinate(4, 1),
        CubeCoordinate(3, 2),
        CubeCoordinate(2, 3),
        CubeCoordinate(1, 3),
        CubeCoordinate(0, 3),
        CubeCoordinate(0, 2),
        CubeCoordinate(0, 1),
        CubeCoordinate(1, 0)
    ]

    invalidCoords5Flat: list[CubeCoordinate] = [
        CubeCoordinate(0, 0),
        CubeCoordinate(1, -1),
        CubeCoordinate(2, -2),
        CubeCoordinate(3, -2),
        CubeCoordinate(4, -2),
        CubeCoordinate(5, -2),
        CubeCoordinate(5, -1),
        CubeCoordinate(5, 0),
        CubeCoordinate(5, 1),
        CubeCoordinate(4, 2),
        CubeCoordinate(3, 3),
        CubeCoordinate(2, 4),
        CubeCoordinate(1, 4),
        CubeCoordinate(0, 4),
        CubeCoordinate(-1, 4),
        CubeCoordinate(-1, 3),
        CubeCoordinate(-1, 2),
        CubeCoordinate(-1, 1)
    ]

    validCoords3: list[CubeCoordinate] = [
        CubeCoordinate(1, 0),
        CubeCoordinate(2, 0),
        CubeCoordinate(2, 1),
        CubeCoordinate(1, 2),
        CubeCoordinate(0, 2),
        CubeCoordinate(0, 1),
    ]

    invalidCoords3: list[CubeCoordinate] = [
        CubeCoordinate(0,  0),
        CubeCoordinate(0, -1),
        CubeCoordinate(2, -1),
        CubeCoordinate(3, -1),
        CubeCoordinate(3,  0),
        CubeCoordinate(3,  1),
        CubeCoordinate(2,  2),
        CubeCoordinate(1,  3),
        CubeCoordinate(0,  3),
        CubeCoordinate(-1, 3),
        CubeCoordinate(-1, 2),
        CubeCoordinate(-1, 1),
    ]

    validCoords5Pointy: list[CubeCoordinate] = [
        CubeCoordinate(1,  0),
        CubeCoordinate(2,  0),
        CubeCoordinate(3,  0),
        CubeCoordinate(3,  1),
        CubeCoordinate(3,  2),
        CubeCoordinate(2,  3),
        CubeCoordinate(1,  4),
        CubeCoordinate(0,  4),
        CubeCoordinate(-1, 4),
        CubeCoordinate(-1, 3),
        CubeCoordinate(-1, 2),
        CubeCoordinate(0,  1)
    ]

    invalidCoords5Pointy: list[CubeCoordinate] = [
        CubeCoordinate(0,  0),
        CubeCoordinate(1, -1),
        CubeCoordinate(2, -1),
        CubeCoordinate(3, -1),
        CubeCoordinate(4, -1),
        CubeCoordinate(4,  0),
        CubeCoordinate(4,  1),
        CubeCoordinate(4,  2),
        CubeCoordinate(3,  3),
        CubeCoordinate(2,  4),
        CubeCoordinate(1,  5),
        CubeCoordinate(0,  5),
        CubeCoordinate(-1, 5),
        CubeCoordinate(-2, 5),
        CubeCoordinate(-2, 4),
        CubeCoordinate(-2, 3),
        CubeCoordinate(-2, 2),
        CubeCoordinate(-1, 1)
    ]

    def test_pointy_3(self):
        strategy = HexagonGridLayoutStrategy()
        coords = strategy.fetch_grid_coords(3, 3, CubeCoordinate.POINTY_TOP)
        self.assertTrue(contains_all(coords, self.validCoords3))
        self.assertTrue(contains_none(coords, self.invalidCoords3))

    def test_flat_3(self):
        strategy = HexagonGridLayoutStrategy()
        coords = strategy.fetch_grid_coords(3, 3, CubeCoordinate.FLAT_TOP)
        self.assertTrue(contains_all(coords, self.validCoords3))
        self.assertTrue(contains_none(coords, self.invalidCoords3))

    def test_pointy_5(self):
        strategy = HexagonGridLayoutStrategy()
        coords = strategy.fetch_grid_coords(5, 5, CubeCoordinate.POINTY_TOP)
        self.assertTrue(contains_all(coords, self.validCoords5Pointy))
        self.assertTrue(contains_none(coords, self.invalidCoords5Pointy))

    def test_flat_5(self):
        strategy = HexagonGridLayoutStrategy()
        coords = strategy.fetch_grid_coords(5, 5, CubeCoordinate.FLAT_TOP)
        self.assertTrue(contains_all(coords, self.validCoords5Flat))
        self.assertTrue(contains_none(coords, self.invalidCoords5Flat))

    def test_check_size(self):
        strategy = HexagonGridLayoutStrategy()
        self.assertIsNone(strategy.check_size(1, 1))

        invalid_pairs = [
            [2, 2],
            [1, 2],
            [0, 0],
            [-1, -1]
        ]

        test_invalid_params(self, strategy, invalid_pairs)


if __name__ == '__main__':
    unittest.main()
