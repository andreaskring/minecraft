from time import sleep
from mcipc.rcon import Client

with Client('localhost', 25575) as client:
    client.login('hurra')
    # client.say('Hej med jer')
    # r = client.run('setblock', '-88 72 84 iron_block')
    x_offset, y_offset, z_offset = -224, 68, 263
    h = 20
    for y in range(h):
        for x in range(y, 2*h - 1 - y):
            for z in range(y, 2*h - 1 - y):
                r = client.run(
                    'setblock',
                    f'{x_offset + x} {y_offset + y} {z_offset + z} sandstone'
                )
                sleep(0.01)
