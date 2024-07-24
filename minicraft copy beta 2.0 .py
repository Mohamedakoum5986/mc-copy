from ursina import *
import random
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from ursina.shaders import lit_with_shadows_shader
from ursina.shaders import basic_lighting_shader
from ursina.shaders import colored_lights_shader
import Treeeeeeee


app = Ursina(development_mode=True)
print('loading ......')
pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
window.fps_counter.enabled = True
window.exit_button.visible = False
window.entity_counter.enabled = False
window.fullscreen = True
window.collider_counter.enabled = False

player = FirstPersonController()
player.gravity =0.4
player.y = 10
player.speed = 7
def fog ():
    scene.fog_density = .1
    scene.fog_color = color.red

arm = Entity(
    parent=camera.ui,
    model='cube',
    texture='Screenshot 2024-07-03 080139.png',
    position=(0.75, -0.6),
    rotation=(150, -10, 6),
    scale=(0.3, 0.3, 1.5)
)

def arm_update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        arm.position = (0.6, -0.5)
    else:
        arm.position = (0.75, -0.6)

hotbar = Entity(
    parent=camera.ui,
    model='quad',
    texture='Screenshot 2024-07-03 160736.png',
    color=color.light_gray,
    position=(0.11, -0.4, 7),
    scale=(0.6, 0.1, 2.5)
)
seed_generator  = random.randint(0,48648646546845)
noise = PerlinNoise(octaves=2, seed=seed_generator)
amp = 13               
freq = 24
render_distance = 5  # Render distance in chunks
chunk_size = 2 # Size of each chunk

chunk_size = 2
render_distance = 3   # render distance in chunks
chunks = {}

def generate_chunk(x, z):
    chunk = []
    for i in range(chunk_size):
        for j in range(chunk_size):
            world_x = x * chunk_size + i
            world_z = z * chunk_size + j
            y = int(noise([world_x / freq, world_z / freq]) * amp)
            chunk.append(create_block((world_x, y, world_z), 'grass texture.png'))
            for k in range(y):
                chunk.append(create_block((world_x, k, world_z), 'grass texture.png'))
                chunk.append(create_block((world_x, k, world_z), 'grass texture.png'))

            for k in range(-1, -6, -1):
                chunk.append(create_block((world_x, k, world_z), 'stone texture.png'))
    chunks[(x, z)] = chunk

def create_block(position, texture):
    return Entity(
        model='grass.obj',
        texture=texture,
        position=position,
        collider='box',
        parent=scene,
        origin_y=0.5,
        color=color.light_gray,
        shader=Sh,
        matirial = ' materials.mtl'
    )

def update_chunks():
    player_chunk = (int(player.x // chunk_size), int(player.z // chunk_size))
    for x in range(player_chunk[0] - render_distance, player_chunk[0] + render_distance + 1):
        for z in range(player_chunk[1] - render_distance, player_chunk[1] + render_distance + 1):
            if (x, z) not in chunks:
                generate_chunk(x, z)
    for chunk_pos in list(chunks.keys()):
        if abs(chunk_pos[0] - player_chunk[0]) > render_distance or abs(chunk_pos[1] - player_chunk[1]) > render_distance:
            for block in chunks[chunk_pos]:
                destroy(block)
            del chunks[chunk_pos]




def input(key):
    if key == 'left mouse down':
        hotbar.texture = 'Screenshot 2024-07-03 155913.png'
        hit_info = raycast(camera.world_position, camera.forward, distance=8)
        if hit_info.hit:
                Tree(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='wood2-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, utoplay=True, auto_destroy=False)


    if key == 'e':
        hotbar.texture = 'Screenshot 2024-07-03 155913.png'
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
                planks(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='wood2-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, autoplay=True, auto_destroy=False)



    if key == 'f':
        hotbar.texture = 'Screenshot 2024-07-03 160328.png'
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
                Dirt(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='grass1.ogg', volume=1, pitch=1, balance=0, loop=False, loops=1, autoplay=True, auto_destroy=False)

    if key == 'r':
        hotbar.texture = 'Screenshot 2024-07-03 160143.png'
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
                Stone(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='stone1-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, autoplay=True, auto_destroy=False)
    
    if key == 'q':
        hotbar.texture = 'Screenshot 2024-07-03 160520.png'
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
                Water(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='stone1-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, autoplay=True, auto_destroy=False)

    if key == 'c':
        hotbar.texture = 'Screenshot 2024-07-03 160736.png'
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
                glass(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='stone1-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, autoplay=True, auto_destroy=False)




    if key == 'right mouse down' and mouse.hovered_entity:
        destroy(mouse.hovered_entity)

    if key == "escape":
        print("exiting ....")      
        exit()


class Dirt (Button):
    def __init__(self, position=(random.randint(1, 25), 1.5, random.randint(1, 25)), texture='grass texture.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='grass.obj',
            texture=texture,
            origin_y=0.5,
            color=color.light_gray,
            shader=Sh,
            
        )


class Water(Button):
    def __init__(self , position=(random.randint(1, 25),1.5, random.randint(1, 25)) ):
        super().__init__(
            parent= scene,
            position = position,
            model= 'water.obj',
            origin_y  = 0.5,
            texture = "water texture.png",
            color = color.white,shader= Sh,




        )
        self.texture_choice = 0
        self.textures = ['Ball_2_Texture.png','3806546.png','Street Fighter II Champion Edition.png',"white_cube"]



class glass(Button):
    def __init__(self , position=(random.randint(1, 25),1.5, random.randint(1, 25)) ):
        super().__init__(
            parent= scene,
            position = position,
            model= 'glass.obj',
            origin_y  = 0.5,
            texture = "glass texture.png",
            color = color.white,shader= Sh,




        )



class Stone(Button):
    def __init__(self ,position = (random.randint(1,25),1.5,random.randint(1,25)) ):
        super().__init__(
            parent= scene,
            position = position,
            model= 'stone.obj',
            origin_y  = 0.5,
            texture = "stone texture.png",
            color= color.light_gray,shader= Sh,


        )
        self.texture_choice = 0
        self.textures = ['Ball_2_Texture.png','3806546.png','Street Fighter II Champion Edition.png',"white_cube"]


class Tree(Button):
    def __init__(self ,position = (random.randint(1,25),1.5,random.randint(1,25)) ):
        super().__init__(
            parent= scene,
            position = position,
            model= 'wood.obj',
            origin_y  = 0.5,
            texture = 'wood texture.png',
            color= color.light_gray,shader= Sh,




        )
        self.texture_choice = 0
        self.textures = ['Ball_2_Texture.png','3806546.png','Street Fighter II Champion Edition.png',"white_cube"]   


class planks(Button):
    def __init__(self ,position = (random.randint(1,25),1.5,random.randint(1,25)) ):
        super().__init__(
            parent= scene,
            position = position,
            model= 'planks.obj',
            origin_y  = 0.5,
            texture = 'plaks texture.png',
            color= color.light_gray,shader= Sh,




        )
        self.texture_choice = 0
        self.textures = ['Ball_2_Texture.png','3806546.png','Street Fighter II Champion Edition.png',"white_cube"]   


def sh_update():
    global Sh
    Sh = basic_lighting_shader
 
sh_update()

skybox_image = load_texture("download (11).jpeg")
sky = Sky(texture=skybox_image)

day_texture = load_texture('download (11).jpeg')
night_texture = load_texture('download (14).jpeg')

def update_skybox():
        sky.texture = day_texture

def update():
    update_skybox()
    arm_update()
    update_chunks()
    fog()
    if player.y < -30:
        player.position=(3,10,3)
    
    for t  in range (10):
        i = random.randint(0,2000)
        if i == 2:
            treeee  = Entity(model= 'treeeee.obj',texture = 'texture.png',origin_y = 1.5,x = random.randint(0,2),z=random.randint(0,200) ,shader = basic_lighting_shader ,collider = 'box')


Audio(sound_file_name='08 - Minecraft.mp3', volume=1, loop=True, autoplay=True, auto_destroy=False)

app.run()