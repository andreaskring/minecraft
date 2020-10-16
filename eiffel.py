import time
from mcipc.rcon import Client
from nbtschematic import SchematicFile


sf = SchematicFile.load('eiffel-tower-e1260.schematic')

with Client('localhost', 25575) as client:
    client.login('hurra')

    shape = sf.blocks.shape

    x_offset, y_offset, z_offset = 5033, 69, 4970
    for y in range(shape[0]):
        for z in range(shape[1]):
            for x in range(shape[2]):
                block = sf.blocks[y, z, x]
                if not block == 0:
                    r = client.run(
                        'setblock',
                        f'{x_offset + x} {y_offset + y} {z_offset + z} air'
                    )
                    # time.sleep(0.03)
