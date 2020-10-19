import unittest
import numpy as np
import tunnel


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

    # def test_next_along_530(self):
    #     lp = tunnel.LatticePath(np.zeros(3), np.array((5, 3, 0)))
    #     lattice_point_iter = iter(lp)
    #
    #     self.assertTrue(np.array_equal(
    #         np.array((1, 0, 0)),
    #         next(lattice_point_iter)
    #     ))
    #     self.assertTrue(np.array_equal(
    #         np.array((2, 2, 2)),
    #         next(lattice_point_iter)
    #     ))
    #     self.assertTrue(np.array_equal(
    #         np.array((3, 3, 3)),
    #         next(lattice_point_iter)
    #     ))
