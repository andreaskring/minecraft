from time import sleep
import numpy as np
from mcipc.rcon import Client
import credentials


class LatticePath(object):

    def __init__(self, r_start, r_end):
        self.r_start = r_start
        self.r_end = r_end
        self.r_current = r_start
        self.direction = r_end - r_start
        self.box = self.generate_box()

    def __iter__(self):
        return self

    def __next__(self):
        if np.linalg.norm(self.r_end - self.r_current) > 0:
            # Get directions pointing the "same" way as self.direction
            r_next_candidates = self.r_current + self.filter_directions()
            # Get distances to line from all next point candidates
            dists_to_line = self.dist(r_next_candidates)
            # Choose the candidate with the shortest distance to the line
            self.r_current = r_next_candidates[np.argmin(dists_to_line)]
            # Update the direction
            self.direction = self.r_end - self.r_current
            return self.r_current
        else:
            raise StopIteration

    @staticmethod
    def generate_box():
        box = np.array((), dtype=np.int8)
        for i in range(-1, 2):
            for j in range(-1, 2):
                for k in range(-1, 2):
                    if not (i == 0 and j == 0 and k == 0):
                        a = np.array((i, j, k))
                        box = np.append(box, a)
        return np.reshape(box, (26, 3))

    def dist(self, point: np.array):
        """
        Distance from point to line defined by r_start and r_end
        :param point: Array of shape (n, 3)
        """
        return np.linalg.norm(
            np.cross(point - self.r_current, self.direction), axis=1) / \
            np.linalg.norm(self.direction)

    def filter_directions(self):
        dot_products = np.matmul(self.box, self.direction)
        return self.box[[True if dp > 0 else False for dp in dot_products]]


lp = LatticePath(np.zeros(3), np.array((5, 0, 0)))
my_iter = iter(lp)
# for n in my_iter:
#     print(n)


# with Client(credentials.hostname, credentials.port) as client:
#     client.login(credentials.password)
#     x_offset, y_offset, z_offset = -220, 68, 204
#     r = 20.5
#     for y in range(int(r)):
#         for x in range(-(int(r) + 1), int(r) + 2):
#             for z in range(-(int(r) + 1), int(r) + 2):
#                 if dist(x, y, z) <= r:
#                     resp = client.run(
#                         'setblock',
#                         f'{x_offset + x} {y_offset + y} {z_offset + z} white_concrete'
#                     )
#                     sleep(0.01)
