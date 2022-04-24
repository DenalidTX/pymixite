import unittest

from mixite.hex import GridData, HexagonImpl
from mixite.coord import CubeCoordinate
from mixite.storage import DefaultHexagonDataStorage


class TestDefaultHexagonDataStorage(unittest.TestCase):
    testCoord = CubeCoordinate(4, 5)
    testData = HexagonImpl(GridData(CubeCoordinate.FLAT_TOP, 1, 10, 10), CubeCoordinate(5, 12))

    def test_add_coords(self):
        storage = DefaultHexagonDataStorage()
        storage.add_coord(self.testCoord)
        self.assertTrue(storage.contains(self.testCoord))
        self.assertIsNone(storage.get_data_for(self.testCoord))

    def test_add_coord_with_data(self):
        storage = DefaultHexagonDataStorage()
        storage.add_coord_with_data(self.testCoord, self.testData)
        self.assertTrue(storage.contains(self.testCoord))
        self.assertTrue(storage.has_data_for(self.testCoord))
        self.assertEqual(self.testData, storage.get_data_for(self.testCoord))

    def test_replace_data(self):
        storage = DefaultHexagonDataStorage()
        replacement_data = HexagonImpl(GridData(CubeCoordinate.FLAT_TOP, 1, 10, 10), CubeCoordinate(5, 13))
        self.assertNotEqual(replacement_data, self.testData)
        storage.add_coord(self.testCoord)
        self.assertTrue(storage.add_coord_with_data(self.testCoord, self.testData))
        self.assertTrue(storage.add_coord_with_data(self.testCoord, replacement_data))
        self.assertEqual(replacement_data, storage.get_data_for(self.testCoord))

    def test_get_nonexistent(self):
        storage = DefaultHexagonDataStorage()
        self.assertIsNone(storage.get_data_for(self.testCoord))

    def test_not_containing(self):
        storage = DefaultHexagonDataStorage()
        self.assertFalse(storage.contains(self.testCoord))


if __name__ == '__main__':
    unittest.main()
