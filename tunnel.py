from time import sleep
import numpy as np
from mcipc.rcon import Client
import credentials


def generate_box(n: int, include_origin=True) -> np.array:
    """
    Generate an array of simple cubic lattice vectors
    :param n: half of the box size in the x-, y- and z-direction
    :param include_origin: weather the origin is included or not
    """
    box = np.array((), dtype=np.int8)
    for i in range(-n, n + 1):
        for j in range(-n, n + 1):
            for k in range(-n, n + 1):
                if not (i == 0 and j == 0 and k == 0 and not include_origin):
                    box = np.append(box, np.array((i, j, k)))

    if include_origin:
        shape = ((2 * n + 1) ** 3, 3)
    else:
        shape = ((2 * n + 1) ** 3 - 1, 3)
    return np.reshape(box, shape)


class LatticePath(object):

    def __init__(self, r_start, r_end):
        self.r_start = r_start
        self.r_end = r_end
        self.r_current = r_start
        self.direction = r_end - r_start
        self.box = generate_box(1, include_origin=False)

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
            return self.r_current
        else:
            raise StopIteration

    def dist(self, point: np.array):
        """
        Distance from point to line defined by r_start and r_end
        :param point: Array of shape (n, 3)
        """
        return np.linalg.norm(
            np.cross(point - self.r_start, self.direction), axis=1) / \
            np.linalg.norm(self.direction)

    def filter_directions(self):
        """
        Get directions pointing the "same" way as self.direction
        """
        dot_products = np.matmul(self.box, self.direction)
        return self.box[[True if dp > 0 else False for dp in dot_products]]


def hemisphere(radius: float) -> np.array:
    box = generate_box(int(radius))
    return box[[True if r[1] >= 0 and np.linalg.norm(r) <= radius else False
                for r in box]]


if __name__ == '__main__':
    start = np.array((-147, 59, 194))
    end = np.array((-218, 59, 205))

    lp = LatticePath(start, end)
    lattice_iter = iter(lp)
    H = hemisphere(2.5)
    with Client(credentials.hostname, credentials.port) as client:
        client.login(credentials.password)
        for point in lattice_iter:
            for h in H:
                client.run(
                    'setblock',
                    f'{point[0] + h[0]} {point[1] + h[1]} {point[2] + h[2]} air'
                )
            sleep(1.5)
