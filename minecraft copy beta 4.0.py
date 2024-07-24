from ursina import*
import random
import pygame 
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from ursina.shaders import lit_with_shadows_shader,basic_lighting_shader


clock=pygame.time.Clock()
app = Ursina(development_mode=True)

blocks  = 1
global Sh
Sh =basic_lighting_shader
cha = False
sun = Entity(model= 'cube',texture = 'air texture.png',y = 500,scale  = 30000)

print('loading ......')
window.fps_counter.enabled = True
window.exit_button.visible = False
window.entity_counter.enabled = True
window.fullscreen = True
window.collider_counter.enabled = False
global player_body
player_body ='steav_2.obj'
player_texture = 'player_2.png'
player = FirstPersonController(model = 'player_1.obj',texture = player_texture,shader = Sh,double_sided=True)
player.gravity =0.4
player.y = 10
player.origin_y = 0.07
player.speed = 7
player.set_collide_mask = 20
player.rotation_y  = 180
player.position = (0,30,0)
camera.y = 0.5
camera.z =0.5
player.scale = (0.9,0.9,0.9)










arm = Entity(
    parent=camera.ui,
    model='arm.obj',
    texture='arm texture.png',
    position=(-0.5, -0.6),
    rotation=(150, -10, 6),
    scale=(0.3, 0.3, 1.5)
     
)
arm.shader = Sh
def arm_update():
    if held_keys['left mouse'] or held_keys['right mouse']:
        arm.position = (0.6, -0.5)
    else:
        arm.position = (0.75, -0.6)


seed_generator  = random.randint(0,48648646546845)
noise = PerlinNoise(octaves=1, seed=seed_generator)
amp = 0.05
freq = 10
CAV_AMP  =-9.9





chunk_size = 1
render_distance = 4*2# render distance in chunks
chunks = {}

def generate_chunk(x, z):
    global y
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
            height2 = int(noise([world_x * height_noise_freq-3, world_z * height_noise_freq]) * height_noise_amp-3)
            # Generate terrain blocks
            for k in range(height):
                if k < height - 1:
                    tx = 'stone texture.png'
                elif k > height - 5:
                    tx = 'snowygrass texture.png'
                else:
                    tx = 'grass texture.png'
                chunk.append(create_block((world_x, k, world_z), tx))
            for k in range(-1, -2, -1):
                chunk.append(create_block((world_x, -k-3+height, world_z),'grass texture.png' ))
            for k in range(-1, -2, -1):
                chunk.append(create_block((world_x, -k-4+height, world_z),'stone texture.png' ))

  
            for k in range(-1, -3, -1):
                chunk.append(create_block((world_x, -k-20+-height2, world_z),'stone texture.png' ))
            # Generate trees with a lower probability to save CPU cycles
            if random.random() < 0.0001:  # Lower probability for tree generation
                generate_tree(chunk,world_x, height-1, world_z)


    chunks[(x, z)] = chunk



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
def should_generate_tree(x, z):
    random.seed((x, z))  # Seed based on coordinates to ensure deterministic behavior
    return random.random() < 0.01
def generate_tree(chunk, x, y, z):
    trunk_height = random.randint(4, 6)
    for i in range(trunk_height):
        chunk.append(create_block((x, y + i, z), 'wood texture.png'))
    
    # Generate leaves
    leaf_height = y + trunk_height
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            if abs(dx) == 2 and abs(dz) == 2:
                continue
            chunk.append(create_block((x + dx, leaf_height, z + dz), 'leaves texture.png'))
    for dx in range(-1, 2):
        for dz in range(-1, 2):
            chunk.append(create_block((x + dx, leaf_height + 1, z + dz), 'leaves texture.png'))
    chunk.append(create_block((x, leaf_height + 2, z), 'leaves texture.png'))












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
        
        hit_info = raycast(camera.world_position, camera.forward, distance=8)
        if hit_info.hit:
            if blocks == 1:
                arm.model = 'wood.obj'
                arm.texture = 'grass texture.png'
                arm.position = (0.75, -0.7)
                arm.rotation = (6, -10, 4)
                Dirt(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='grass1.ogg', volume=1, pitch=1, balance=0, loop=False, loops=1, utoplay=True, auto_destroy=False)

            if blocks == 2:
                arm.model = 'wood.obj'
                arm.texture = 'wood texture.png'
                arm.position = (0.75, -0.7)
                arm.rotation = (6, -10, 4)
                Tree(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='wood2-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, utoplay=True, auto_destroy=False)

            if blocks == 3:
                arm.model = 'wood.obj'
                arm.texture = 'stone texture.png'
                arm.position = (0.75, -0.7)
                arm.rotation = (6, -10, 4)
                Stone(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='stone1-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, utoplay=True, auto_destroy=False)


            if blocks == 4:
                arm.model = 'wood.obj'
                arm.texture = 'water texture.png'
                arm.position = (0.75, -0.7)
                arm.rotation = (6, -10, 4)
                Water(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='wood2-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, utoplay=True, auto_destroy=False)

            if blocks == 5:
                arm.model = 'wood.obj'
                arm.texture = 'glass texture.png'
                arm.position = (0.75, -0.7)
                arm.rotation = (6, -10, 4)
                glass(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='wood2-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, utoplay=True, auto_destroy=False)


            if blocks == 6:
                arm.model = 'wood.obj'
                arm.texture = 'plaks texture.png'
                arm.position = (0.75, -0.7)
                arm.rotation = (6, -10, 4)
                planks(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='wood2-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, utoplay=True, auto_destroy=False)

            if blocks == 7:
                arm.model = 'wood.obj'
                arm.texture = 'snowygrass texture.png'
                arm.position = (0.75, -0.7)
                arm.rotation = (6, -10, 4)
                snowy_grassblock(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='grass1.ogg', volume=1, pitch=1, balance=0, loop=False, loops=1, utoplay=True, auto_destroy=False)

            if blocks == 8:
                arm.model = 'wood.obj'
                arm.texture = 'leaves texture.png'
                arm.position = (0.75, -0.7)
                arm.rotation = (6, -10, 4)
                leaves(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='step5.ogg', volume=1, pitch=1, balance=0, loop=False, loops=1, utoplay=True, auto_destroy=False)




    if key == 'right mouse down' and mouse.hovered_entity:
        destroy(mouse.hovered_entity)



    if held_keys['f3']:
        camera.z = -4

    if held_keys['f1']:
        camera.z = 0.5

    if held_keys['f2']:
        for i in range(100): 
            Tree_update()


    if held_keys['shift']: 
        player.model = 'player_2.obj'
        camera.y = 0.5

    if not held_keys['shift']:
        player.model = 'player_1.obj'
        camera.y = 0

    if held_keys['w']:
        player.model = 'player walk.obj'
        

    if not  held_keys['w']:
        player.model = 'player_1.obj'


    if  key == 'left mouse down' :
        player.model = 'player distroy.obj'
    if  key == 'right mouse down' :
        player.model = 'player distroy.obj'




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
            color=color.white,
            shader=Sh,
            
            
        )
        
class youpy (Button):
    def __init__(self, position=(random.randint(1, 25), 1.5, random.randint(1, 25)), texture='grass texture.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='youpy.obj',
            texture='youpy texture.png',
            origin_y=0.1,
            color=color.white,
            shader=Sh,
            scale = 0.5,
            collider= Sh

            
            
        )




class leaves (Button):
    def __init__(self, position=(random.randint(1, 25), 1.5, random.randint(1, 25)), texture='grass texture.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='grass.obj',
            texture='leaves texture.png',
            origin_y=0.5,
            color=color.white,
            shader=Sh,
            
        )




class snowy_grassblock (Button):
    def __init__(self, position=(random.randint(1, 25), 1.5, random.randint(1, 25)), texture='grass texture.png'):
        super().__init__(
            parent=scene,
            position=position,
            model='grass.obj',
            collider = 'grass.obj',
            texture='snowygrass texture.png',
            origin_y=0.5,
            color=color.white,
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
            color = color.white,
            shader= Sh,





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
            color = color.white,
            shader= Sh,




        )
        


class sapling(Button):
    def __init__(self , position=(random.randint(1, 25),1.5, random.randint(1, 25)) ):
        super().__init__(
            parent= scene,
            position = position,
            model= 'popy model.obj',
            origin_y  = 0.1,
            texture = 'popyy texture.png',
            scale = 0.5,
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
            color= color.white,
            shader= Sh,


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
            color=color.white,
            shader= Sh,




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
            color= color.white,
            shader= Sh,




        )
        self.texture_choice = 0
        self.textures = ['Ball_2_Texture.png','3806546.png','Street Fighter II Champion Edition.png',"white_cube"]   




skybox_image = load_texture("download (11).jpeg")
sky = Sky(texture=skybox_image)

day_texture = load_texture('download (11).jpeg')
night_texture = load_texture('download (14).jpeg')

def update_skybox():
        sky.texture = day_texture





def update():
    global blocks
    arm_update()
    update_chunks()
    arm_update()
    update_chunks()


    if player.y < -90:
        player.position = (3, 70, 5)

    # Existing key checks and player logic...

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

    sun.position.x = player.position.x
    

Audio(sound_file_name='08 - Minecraft.mp3', volume=1, loop=True, autoplay=True, auto_destroy=False)

directional_light = DirectionalLight(color=color.white10, shadows=cha)
directional_light.intensity = 0.5

app.run()
