# chunk_generator.py
import random
from perlin_noise import PerlinNoise

def generate_chunk(x, z, chunk_size=1, freq=13, amp=10, CAV_AMP=-9.9):
    seed_generator = random.randint(0, 48648646546845)
    noise = PerlinNoise(octaves=2, seed=seed_generator)

    chunk = []
    for i in range(chunk_size):
        for j in range(chunk_size):
            world_x = x * chunk_size + i
            world_z = z * chunk_size + j

            y = int(noise([world_x / freq, world_z / freq]) * amp)
            c = int(noise([world_x / freq, world_z / freq]) * CAV_AMP)

            # Generate blocks and return
            block_data = [(world_x, y, world_z), 'grass texture.png']
            for k in range(-1, -5, -1):
                block_data.append((world_x, k + y - 0.002, world_z, 'stone texture.png'))
            for k in range(-1, -3, -1):
                block_data.append((world_x, -k - 15 + c, world_z, 'stone texture.png'))
                
            chunk.append(block_data)

    return chunk
