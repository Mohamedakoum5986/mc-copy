from ursina import *
import random
import time
from ursina.prefabs.first_person_controller import FirstPersonController
from sys import exit
from perlin_noise import PerlinNoise
from ursina.shaders import basic_lighting_shader

app = Ursina()
print('loading ......')

window.fps_counter.enabled = True
window.exit_button.visible = False
window.fullscreen = True
window.entity_counter.enabled  = False
window.collider_counter.enabled = False



player = FirstPersonController()
player.gravity = 0.3
scene.fog_density = 1.0
scene.fog_color = color.gray


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
    
hotbare= Entity(
    parent = camera.ui,
    model = 'quad',
    texture = 'Screenshot 2024-07-03 160736.png',
    color= color.light_gray,
    position= (0.11,-0.4,7),
    scale= (0.6,0.1,2.5)
)
seed_generator = random.randint(0,4546518121651546816548615)

noise = PerlinNoise(octaves =2,seed = seed_generator)
amp = 9
freq = 24

render_distance = 20

def generate_terrain():
    for x in range(render_distance):
        for z in range(render_distance):
            y = int(noise([x / freq, z / freq]) * amp)
            create_block((x, y, z), 'download (8).jpeg')
            for i in range(y):
                create_block((x, i, z), 'download (8).jpeg')
            for i in range(-1, -4, -1):
                create_block((x, i, z), 'download (9).jpeg')

def create_block(position, texture):
    Entity(
        model='cube',
        texture=texture,
        position=position,
        collider='box',
        parent=scene,
        origin_y=0.5,
        color= color.light_gray,
        shader=basic_lighting_shader,
        matirial = ' materials.mtl'
    )

generate_terrain()



class Dirt(Button):
    def __init__(self ,position = (random.randint(1,25),1.5,random.randint(1,25)) ):
        super().__init__(
            parent= scene,
            position = position,
            model= 'cube',
            origin_y  = 0.5,
            texture = "download (8).jpeg",
            color=color.light_gray,shader= basic_lighting_shader,


        )
        self.texture_choice = 0
        self.textures = ['Ball_2_Texture.png','3806546.png','Street Fighter II Champion Edition.png',"white_cube"]

class Tree(Button):
    def __init__(self ,position = (random.randint(1,25),1.5,random.randint(1,25)) ):
        super().__init__(
            parent= scene,
            position = position,
            model= 'cube',
            origin_y  = 0.5,
            texture = "download (2).png",
            color= color.light_gray,shader= basic_lighting_shader,


        )
        self.texture_choice = 0
        self.textures = ['Ball_2_Texture.png','3806546.png','Street Fighter II Champion Edition.png',"white_cube"]

class Stone(Button):
    def __init__(self ,position = (random.randint(1,25),1.5,random.randint(1,25)) ):
        super().__init__(
            parent= scene,
            position = position,
            model= 'cube',
            origin_y  = 0.5,
            texture = "download (9).jpeg",
            color= color.light_gray,shader= basic_lighting_shader,


        )
        self.texture_choice = 0
        self.textures = ['Ball_2_Texture.png','3806546.png','Street Fighter II Champion Edition.png',"white_cube"]

class Water(Button):
    def __init__(self ,position = (random.randint(1,25),1.5,random.randint(1,25)) ):
        super().__init__(
            parent= scene,
            position = position,
            model= 'cube',
            origin_y  = 0.5,
            texture = "download (13).jpeg",
            color = color.light_gray,shader= basic_lighting_shader,



        )
        self.texture_choice = 0
        self.textures = ['Ball_2_Texture.png','3806546.png','Street Fighter II Champion Edition.png',"white_cube"]





   # def input(self, key):
  #          if key == " b":
  #              self.texture_choice +=1
 #               self.texture_choice %= len(self.textures)
 #               self.texture = self.textures[self.texture_choice]
 #               position = (random.randint(1,25),1.5,random.randint(1,25))


def input(key):
    if key == 'left mouse down':
        hotbare.texture = 'Screenshot 2024-07-03 155913.png'
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
                Tree(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='wood2-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, utoplay=True, auto_destroy=False)
                

    if key == 'f':
        hotbare.texture = 'Screenshot 2024-07-03 160328.png'
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
                Dirt(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='grass1.ogg', volume=1, pitch=1, balance=0, loop=False, loops=1, autoplay=True, auto_destroy=False)

    if key == 'e':
        hotbare.texture = 'Screenshot 2024-07-03 160143.png'
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
                Stone(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='stone1-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, autoplay=True, auto_destroy=False)
    
    if key == 'q':
        hotbare.texture = 'Screenshot 2024-07-03 160520.png'
        hit_info = raycast(camera.world_position, camera.forward, distance=5)
        if hit_info.hit:
                Water(position=hit_info.entity.position + hit_info.normal)
                Audio(sound_file_name='stone1-step-101soundboards.mp3', volume=1, pitch=1, balance=0, loop=False, loops=1, autoplay=True, auto_destroy=False)


    if key == 'right mouse down' and mouse.hovered_entity:
        destroy(mouse.hovered_entity)

    if key == "escape":
        print("exiting ....")      
        exit()


chiken = Entity(model = 'minecraft-chicken\source\chicken.fbx',texture = 'chicken.png',double_sided=True,scale = 0.07,y = 0.6,z= render_distance/2,shader= basic_lighting_shader)

skybox_image2= load_texture("download (11).jpeg")
skybox_image = load_texture("download (11).jpeg")

pivot = Entity()
DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
sky = Sky()


day_texture = load_texture('download (11).jpeg')
night_texture = load_texture('download (14).jpeg')

arm_update()


def update_skybox():
    current_time = time.time() % 1000
    if current_time < 5:
        sky.texture = night_texture
    else:
        sky.texture = day_texture


Tree()
def update():
    update_skybox()
    if player.y < -4 :
        player.x=10
        player.y = 3
    chiken.look_at(player,'forward')
    chiken.rotation_x = 0
    arm_update()

Audio(sound_file_name='08 - Minecraft.mp3', volume=1, pitch=1, balance=0, loop=True, loops=1, autoplay=True, auto_destroy=False)




app.run()