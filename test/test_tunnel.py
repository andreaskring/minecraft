import unittest
import numpy as np
import tunnel


class TestGenerateBox(unittest.TestCase):

    def test_n_is_1_origin_included(self):
        box = tunnel.generate_box(1)
        # Assert a random sample
        self.assertTrue(np.array_equal(np.array((-1, -1, -1)), box[0]))
        self.assertTrue(np.array_equal(np.array((-1, 1, 1)), box[8]))
        self.assertTrue(np.array_equal(np.array((0, 0, -1)), box[12]))
        self.assertTrue(np.array_equal(np.array((0, 0, 0)), box[13]))
        self.assertTrue(np.array_equal(np.array((1, 0, -1)), box[21]))
        self.assertTrue(np.array_equal(np.array((1, 1, 1)), box[26]))

    def test_n_is_1_origin_not_included(self):
        box = tunnel.generate_box(1, include_origin=False)
        # Assert a random sample
        self.assertTrue(np.array_equal(np.array((-1, -1, -1)), box[0]))
        self.assertTrue(np.array_equal(np.array((-1, 1, 1)), box[8]))
        self.assertTrue(np.array_equal(np.array((0, 0, -1)), box[12]))
        self.assertTrue(np.array_equal(np.array((1, 0, -1)), box[20]))
        self.assertTrue(np.array_equal(np.array((1, 1, 1)), box[25]))

    def test_n_is_2_origin_included(self):
        box = tunnel.generate_box(2)
        # Assert a random sample
        self.assertTrue(np.array_equal(np.array((-2, -2, -2)), box[0]))
        self.assertTrue(np.array_equal(np.array((-1, -1, 0)), box[32]))
        self.assertTrue(np.array_equal(np.array((0, 0, 0)), box[62]))
        self.assertTrue(np.array_equal(np.array((0, 2, -2)), box[70]))
        self.assertTrue(np.array_equal(np.array((2, -2, 1)), box[103]))
        self.assertTrue(np.array_equal(np.array((2, 1, 1)), box[118]))
        self.assertTrue(np.array_equal(np.array((2, 2, 2)), box[124]))

    def test_n_is_2_origin_not_included(self):
        box = tunnel.generate_box(2, include_origin=False)
        # Assert a random sample
        self.assertTrue(np.array_equal(np.array((-2, -2, -2)), box[0]))
        self.assertTrue(np.array_equal(np.array((-1, -1, 0)), box[32]))
        self.assertTrue(np.array_equal(np.array((0, 2, -2)), box[69]))
        self.assertTrue(np.array_equal(np.array((2, -2, 1)), box[102]))
        self.assertTrue(np.array_equal(np.array((2, 1, 1)), box[117]))
        self.assertTrue(np.array_equal(np.array((2, 2, 2)), box[123]))


class TestLatticePath(unittest.TestCase):

    def setUp(self) -> None:
        self.r0 = np.array((1, 1, -3))
        self.r1 = np.array((1, 4, 1))
        self.lp = tunnel.LatticePath(self.r0, self.r1)

    def test_dist_is_sqrt41_over_5(self):
        self.assertAlmostEqual(
            np.math.sqrt(41)/5,
            self.lp.dist(np.array((2, 0, -3), ndmin=2))
        )

    def test_dist_is_zero(self):
        self.assertAlmostEqual(0, self.lp.dist(np.reshape(self.r0, (1, 3))))
        self.assertAlmostEqual(0, self.lp.dist(np.reshape(self.r1, (1, 3))))

    def test_box(self):
        box = np.array(
            (
                (-1, -1, -1),
                (-1, -1, 0),
                (-1, -1, 1),
                (-1, 0, -1),
                (-1, 0, 0),
                (-1, 0, 1),
                (-1, 1, -1),
                (-1, 1, 0),
                (-1, 1, 1),
                (0, -1, -1),
                (0, -1, 0),
                (0, -1, 1),
                (0, 0, -1),
                (0, 0, 1),
                (0, 1, -1),
                (0, 1, 0),
                (0, 1, 1),
                (1, -1, -1),
                (1, -1, 0),
                (1, -1, 1),
                (1, 0, -1),
                (1, 0, 0),
                (1, 0, 1),
                (1, 1, -1),
                (1, 1, 0),
                (1, 1, 1)
            )
        )
        self.assertTrue(np.array_equal(box, self.lp.box))

    def test_filter_directions(self):
        lp = tunnel.LatticePath(np.zeros(3), np.array((1, 0, 0)))
        expected_directions = np.array(
            (
                (1, -1, -1),
                (1, -1, 0),
                (1, -1, 1),
                (1, 0, -1),
                (1, 0, 0),
                (1, 0, 1),
                (1, 1, -1),
                (1, 1, 0),
                (1, 1, 1)
            )
        )
        self.assertTrue(np.array_equal(
            expected_directions,
            lp.filter_directions()
        ))

    def test_next_along_100(self):
        lp = tunnel.LatticePath(np.zeros(3), np.array((3, 0, 0)))
        lattice_point_iter = iter(lp)

        self.assertTrue(np.array_equal(
            np.array((1, 0, 0)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((2, 0, 0)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((3, 0, 0)),
            next(lattice_point_iter)
        ))
        with self.assertRaises(StopIteration):
            next(lattice_point_iter)

    def test_next_along_110(self):
        lp = tunnel.LatticePath(np.zeros(3), np.array((3, 3, 0)))
        lattice_point_iter = iter(lp)

        self.assertTrue(np.array_equal(
            np.array((1, 1, 0)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((2, 2, 0)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((3, 3, 0)),
            next(lattice_point_iter)
        ))
        with self.assertRaises(StopIteration):
            next(lattice_point_iter)

    def test_next_along_101(self):
        lp = tunnel.LatticePath(np.zeros(3), np.array((3, 0, 3)))
        lattice_point_iter = iter(lp)

        self.assertTrue(np.array_equal(
            np.array((1, 0, 1)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((2, 0, 2)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((3, 0, 3)),
            next(lattice_point_iter)
        ))
        with self.assertRaises(StopIteration):
            next(lattice_point_iter)

    def test_next_along_111(self):
        lp = tunnel.LatticePath(np.zeros(3), np.array((3, 3, 3)))
        lattice_point_iter = iter(lp)

        self.assertTrue(np.array_equal(
            np.array((1, 1, 1)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((2, 2, 2)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((3, 3, 3)),
            next(lattice_point_iter)
        ))
        with self.assertRaises(StopIteration):
            next(lattice_point_iter)

    def test_next_along_530(self):
        lp = tunnel.LatticePath(np.zeros(3), np.array((5, 3, 0)))
        lattice_point_iter = iter(lp)

        self.assertTrue(np.array_equal(
            np.array((1, 1, 0)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((2, 1, 0)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((3, 2, 0)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((4, 2, 0)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((5, 3, 0)),
            next(lattice_point_iter)
        ))
        with self.assertRaises(StopIteration):
            next(lattice_point_iter)

    def test_next_along_210(self):
        lp = tunnel.LatticePath(np.zeros(3), np.array((2, 1, 0)))
        lattice_point_iter = iter(lp)

        # The point (1, 0, 0) happens to be first in the list of distances,
        # but the point (1, 1, 0) is equally close to the line.
        self.assertTrue(np.array_equal(
            np.array((1, 0, 0)),
            next(lattice_point_iter)
        ))
        self.assertTrue(np.array_equal(
            np.array((2, 1, 0)),
            next(lattice_point_iter)
        ))
        with self.assertRaises(StopIteration):
            next(lattice_point_iter)
