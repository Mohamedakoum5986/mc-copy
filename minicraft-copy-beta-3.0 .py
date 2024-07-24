from ursina import*
import random
import pygame 
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
from ursina.shaders import basic_lighting_shader



clock=pygame.time.Clock()
app = Ursina(development_mode=True)

blocks  = 1


print('loading ......')
window.fps_counter.enabled = True
window.exit_button.visible = False
window.entity_counter.enabled = False
window.fullscreen = True
window.collider_counter.enabled = False

player = FirstPersonController(model  = 'rectangle',scale = 1,exture = 'steve.png',shader = basic_lighting_shader,double_sided=True)
player.gravity =0.4
player.y = 10
player.speed = 7
player.scale = 0.7
player.position = (0,30,0)
camera.z = 0





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


seed_generator  = random.randint(0,48648646546845)
noise = PerlinNoise(octaves=2, seed=seed_generator)
amp = 10
freq = 13
CAV_AMP  =-5




chunk_size = 1
render_distance = 6# render distance in chunks
chunks = {}

def generate_chunk(x, z):
    global y
    chunk = []
    for i in range(chunk_size):
        for j in range(chunk_size):
            world_x = x * chunk_size + i
            world_z = z * chunk_size + j

            y = int(noise([world_x / freq, world_z / freq]) * amp)
            c = int(noise([world_x / freq, world_z / freq]) * CAV_AMP)


            tx =  'grass texture.png'
            if y > 1:
              tx ='snowygrass texture.png'
     
            chunk.append(create_block((world_x, y, world_z),tx))
            for k in range(-1, -5, -1):
                chunk.append(create_block((world_x, k+y-0.002, world_z), 'stone texture.png'))

            tx1 = 'stone texture.png'

            for k in range(-1, -4, -1):
                chunk.append(create_block((world_x, -k-10+c, world_z), tx1))


             
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



   


def Tree_update():
    for t  in range (30):
        i = random.randint(0,2000)
        if i == 1:
            x =random.randint(-1000,1000)
            z =random.randint(-1000,2000)
            Tree(position=  (x,1,z))
            Tree(position=  (x,2,z))
            Tree(position=  (x,3,z))
            Dirt(position=(x,4,z),texture='leaves texture.png')
            Dirt(position=(x,5,z),texture='leaves texture.png')
            Dirt(position=(x+1,5,z+1),texture='leaves texture.png')
            Dirt(position=(x-1,5,z-1),texture='leaves texture.png')


            Dirt(position=(x,6,z),texture='leaves texture.png')


            Dirt(position=(x-1,5,z-1),texture='leaves texture.png')
            Dirt(position=(x-1,5,z+1),texture='leaves texture.png')
          
            Dirt(position=(x+1,5,z-1),texture='leaves texture.png')
                
            Dirt(position=(x+1,4,z+1),texture='leaves texture.png')
            Dirt(position=(x-1,4,z+1),texture='leaves texture.png')
            Dirt(position=(x-0,4,z+1),texture='leaves texture.png')


            Dirt(position=(x+1,4,z-1),texture='leaves texture.png')
            Dirt(position=(x+0,4,z-1),texture='leaves texture.png')


            Dirt(position=(x-1,4,z-1),texture='leaves texture.png')
            Dirt(position=(x+1,4,z-0),texture='leaves texture.png')

            Dirt(position=(x-1,4,z-0),texture='leaves texture.png')
            Dirt(position=(x-2,4,z-0),texture='leaves texture.png')
            Dirt(position=(x-2,4,z-1),texture='leaves texture.png')
            Dirt(position=(x-2,4,z+1),texture='leaves texture.png')

            Dirt(position=(x+2,4,z-0),texture='leaves texture.png')
            Dirt(position=(x+2,4,z-1),texture='leaves texture.png')
            Dirt(position=(x+2,4,z+1),texture='leaves texture.png')

            Dirt(position=(x-2,4,z-2),texture='leaves texture.png')
            Dirt(position=(x-1,4,z-2),texture='leaves texture.png')
            Dirt(position=(x-0,4,z-2),texture='leaves texture.png')
            Dirt(position=(x+1,4,z-2),texture='leaves texture.png')
            Dirt(position=(x+2,4,z-2),texture='leaves texture.png')



            Dirt(position=(x+2,4,z+2),texture='leaves texture.png')
            Dirt(position=(x+1,4,z+2),texture='leaves texture.png')
            Dirt(position=(x+0,4,z+2),texture='leaves texture.png')
            Dirt(position=(x-1,4,z+2),texture='leaves texture.png')
            Dirt(position=(x-2,4,z+2),texture='leaves texture.png')



Tree_update()



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
            collider= 'youpy.obj'

            
            
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
    global blocks
    arm_update()
    update_chunks()
    if player.y < -30:
        player.position = (3, 30, 5)

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

    



     





Audio(sound_file_name='08 - Minecraft.mp3', volume=1, loop=True, autoplay=True, auto_destroy=False)



app.run()

