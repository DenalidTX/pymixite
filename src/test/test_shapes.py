from unittest import TestCase, main
from src.mixite.shapes import Point, Rectangle


class TestPoint(TestCase):

    def test_store_coords(self):
        x = 15
        z = 29
        coord = Point(x, z)
        self.assertEqual(x, coord.coordX)
        self.assertEqual(z, coord.coordY)

    def test_calculate_distance(self):
        """With a distance of 5,12 the hypotenuse should be 13"""
        x1 = 6.5
        y1 = 3.36

        x2 = 11.5
        y2 = 15.36

        distance = Point(x1, y1).distance_from(Point(x2, y2))
        self.assertEqual(13.0, distance)


rect_left = 3.5
rect_top = 9.7
rect_width = 47.3
rect_height = 82.0
rect_right = rect_width + rect_left
rect_bottom = rect_height + rect_top


def default_rect():
    return Rectangle(rect_left, rect_top, rect_width, rect_height)


class TestRectangle(TestCase):

    def test_store_info(self):
        rect = default_rect()
        self.assertEqual(rect_left, rect.left)
        self.assertEqual(rect_top, rect.top)
        self.assertEqual(rect_width, rect.width)
        self.assertEqual(rect_height, rect.height)

    def test_calc_dimensions(self):
        rect = default_rect()
        self.assertEqual(rect_right, rect.right())
        self.assertEqual(rect_bottom, rect.bottom())

    def test_contains_coord(self):
        rect = default_rect()
        self.assertFalse(rect.contains_coords(3.49, 50))
        self.assertTrue(rect.contains_coords(3.5, 50))

        self.assertTrue(rect.contains_coords(50.8, 50))
        self.assertFalse(rect.contains_coords(50.81, 50))

        self.assertFalse(rect.contains_coords(20, 9.69))
        self.assertTrue(rect.contains_coords(20, 9.7))

        self.assertTrue(rect.contains_coords(20, 91.7))
        self.assertFalse(rect.contains_coords(20, 91.71))

    def test_contains_rect(self):
        rect = default_rect()
        rect2 = Rectangle(10.0, 10.0, 30.0, 30.0)
        rect3 = Rectangle(11.0, 11.0, 50.0, 50.0)
        self.assertTrue(rect.contains_rectangle(rect))
        self.assertTrue(rect.contains_rectangle(rect2))
        self.assertFalse(rect.contains_rectangle(rect3))

    def test_overlaps(self):
        rect = default_rect()
        rect2 = Rectangle(0.0, 0.0, 50.0, 50.0)
        rect3 = Rectangle(50.0, 50.0, 50.0, 50.0)
        rect4 = Rectangle(0, 0, 3.5, 80)
        rect5 = Rectangle(50, 50, 10, 10)
        self.assertTrue(rect.overlaps_rectangle(rect))
        self.assertTrue(rect.overlaps_rectangle(rect2))
        self.assertTrue(rect.overlaps_rectangle(rect3))
        self.assertFalse(rect.overlaps_rectangle(rect4))
        self.assertTrue(rect.overlaps_rectangle(rect5))

        self.assertTrue(rect2.overlaps_rectangle(rect))
        self.assertTrue(rect3.overlaps_rectangle(rect))
        self.assertFalse(rect4.overlaps_rectangle(rect))
        self.assertTrue(rect5.overlaps_rectangle(rect))

    def test_aspect_ratio(self):
        rect = Rectangle(0, 0, 1920, 1080)
        self.assertEqual(16.0/9.0, rect.aspect_ratio())


if __name__ == '__main__':
    main()
