from math import sqrt
from time import sleep
from mcipc.rcon import Client
import credentials


def dist(x, y, z):
    return sqrt(x**2 + y**2 + z**2)


with Client(credentials.hostname, credentials.port) as client:
    client.login(credentials.password)
    x_offset, y_offset, z_offset = -220, 68, 204
    r = 20.5
    for y in range(int(r)):
        for x in range(-(int(r) + 1), int(r) + 2):
            for z in range(-(int(r) + 1), int(r) + 2):
                if dist(x, y, z) <= r:
                    resp = client.run(
                        'setblock',
                        f'{x_offset + x} {y_offset + y} {z_offset + z} white_concrete'
                    )
                    sleep(0.01)
