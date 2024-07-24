from ursina import *
import random
import pygame
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from ursina.shaders import lit_with_shadows_shader
from threading import Thread, Event, Lock
from queue import Queue

# Initialize the Ursina app
app = Ursina(development_mode=True)

# Set up threading
chunk_queue = Queue()
update_queue = Queue()
stop_event = Event()
update_lock = Lock()

# Initialize game objects
blocks = 1
Sh = lit_with_shadows_shader
sun = Entity(model='cube', texture='air texture.png', y=500, scale=3000)

window.fps_counter.enabled = True
window.exit_button.visible = False
window.entity_counter.enabled = False
window.fullscreen = True
window.collider_counter.enabled = False

player_texture = 'player_2.png'
player = FirstPersonController(model='player_1.obj', texture=player_texture, shader=Sh, double_sided=True)
player.gravity = 0.4
player.y = 10
player.origin_y = 0.1
player.speed = 7
player.set_collide_mask = 20
player.rotation_y = 180
player.position = (0, 30, 0)
camera.y = 0.5
camera.z = 0.5
player.scale = 1

arm = Entity(
    parent=camera.ui,
    model='arm.obj',
    texture='arm texture.png',
    position=(-0.5, -0.6),
    rotation=(150, -10, 6),
    scale=(0.3, 0.3, 1.5)
)

def arm_update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        arm.position = (0.6, -0.5)
    else:
        arm.position = (0.75, -0.6)

seed_generator = random.randint(0, 48648646546845)
noise = PerlinNoise(octaves=1, seed=seed_generator)
amp = 0.05
freq = 10
CAV_AMP = -9.9

chunk_size = 2
render_distance = 3  # Render distance in chunks
chunks = {}

def generate_chunk(x, z):
    chunk = []

    # Parameters for noise
    height_noise_freq = 0.05
    height_noise_amp = 20

    # Generate terrain height using Perlin noise
    for i in range(chunk_size):
        for j in range(chunk_size):
            world_x = x * chunk_size + i
            world_z = z * chunk_size + j
            
            # Compute terrain height
            height = int(noise([world_x * height_noise_freq, world_z * height_noise_freq]) * height_noise_amp)
            
            # Generate terrain blocks
            for k in range(height):
                if k < height - 5:
                    tx = 'stone texture.png'
                elif k < height - 1:
                    tx = 'dirt texture.png'
                elif k > height - 3:
                    tx = 'snowygrass texture.png'
                else:
                    tx = 'grass texture.png'
                chunk.append(create_block((world_x, k, world_z), tx))
            for k in range(-1, -2, -1):
                chunk.append(create_block((world_x, -k-3+height, world_z), 'grass texture.png'))
            for k in range(-1, -2, -1):
                chunk.append(create_block((world_x, -k-4+height, world_z), 'stone texture.png'))
            for k in range(-1, -2, -1):
                chunk.append(create_block((world_x, -k-5+height, world_z), 'stone texture.png'))
            for k in range(-1, -5, -1):
                chunk.append(create_block((world_x, -k-20+-height, world_z), 'stone texture.png'))
            for k in range(-1, -2, -1):
                chunk.append(create_block((world_x, -k-21+-height, world_z), 'stone texture.png'))

    # Add trees
    for _ in range(2):  # Adjust number of trees
        tree_x = x * chunk_size + random.randint(0, chunk_size - 1)
        tree_z = z * chunk_size + random.randint(0, chunk_size - 1)
        tree_y = int(noise([tree_x * height_noise_freq, tree_z * height_noise_freq]) * height_noise_amp) - 2
        
        if tree_y > 5:
            # Add trunk
            for t in range(4):  # Tree height
                chunk.append(create_block((tree_x, tree_y + t, tree_z), 'wood texture.png'))
            chunk.append(create_block((tree_x, tree_y + t + 2, tree_z), 'leaves texture.png'))
            # Add leaves
            for dx in range(-4, 4):
                for dz in range(-3, 4):
                    if dx**2 + dz**2 < 4:
                        chunk.append(create_block((tree_x + dx, tree_y + 4, tree_z + dz), 'leaves texture.png'))

    return chunk

def create_block(position, texture):
    return Entity(
        model='grass.obj',
        texture=texture,
        position=position,
        collider='stone.obj',
        parent=scene,
        origin_y=0.5,
        color=color.white,
        shader=Sh,
    )

def chunk_worker():
    while not stop_event.is_set():
        try:
            x, z = chunk_queue.get(timeout=1)
            chunk_data = generate_chunk(x, z)
            with update_lock:
                update_queue.put((x, z, chunk_data))
        except Queue.Empty:
            continue
        finally:
            chunk_queue.task_done()

# Start worker threads
for _ in range(4):  # Number of worker threads
    Thread(target=chunk_worker, daemon=True).start()

def update_chunks():
    while not update_queue.empty():
        x, z, chunk_data = update_queue.get()
        with update_lock:
            if (x, z) not in chunks:
                chunks[(x, z)] = chunk_data
            else:
                for block in chunks[(x, z)]:
                    destroy(block)
                chunks[(x, z)] = chunk_data

def update():
    global blocks
    arm_update()
    update_chunks()
    if player.y < -90:
        player.position = (3, 70, 5)

    if held_keys['1']:
        blocks = 1

    if held_keys['2']:
        blocks = 2

    if held_keys['3']:
        blocks = 3

    if held_keys['4']:
        blocks = 4

    if held_keys['5']:
        blocks = 5

    if held_keys['6']:
        blocks = 6

    if held_keys['7']:
        blocks = 7

    if held_keys['8']:
        blocks = 8

    if held_keys['9']:
        blocks = 9

    if chunk_queue.empty():
        player_chunk = (int(player.x // chunk_size), int(player.z // chunk_size))
        for x in range(player_chunk[0] - render_distance, player_chunk[0] + render_distance + 1):
            for z in range(player_chunk[1] - render_distance, player_chunk[1] + render_distance + 1):
                if (x, z) not in chunks:
                    chunk_queue.put((x, z))

    sun.position.x = player.position.x

# Define entities
class Dirt(Button):
    def __init__(self, position=(random.randint(1, 25), 1.5, random.randint(1, 25)), texture='grass texture.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='grass.obj',
            texture=texture,
            origin_y=0.5,
            color=color.white,
            shader=Sh,
        )

# Define other entities as before...

skybox_image = load_texture("download (11).jpeg")
sky = Sky(texture=skybox_image)
day_texture = load_texture('download (11).jpeg')
night_texture = load_texture('download (14).jpeg')

def update_skybox():
    sky.texture = day_texture

# Add music
Audio(sound_file_name='08 - Minecraft.mp3', volume=1, loop=True, autoplay=True, auto_destroy=False)

directional_light = DirectionalLight(color=color.white, shadows=True)
directional_light.intensity = 5

app.run()

# Stop threads gracefully
stop_event.set()
