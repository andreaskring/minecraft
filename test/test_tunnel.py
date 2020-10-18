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
