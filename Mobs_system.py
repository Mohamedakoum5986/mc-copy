from ursina import *
from ursina.shaders import basic_lighting_shader
# Define the cow entity
cow = FrameAnimation3d('cow_walk_', fps=3)
cow.texture = 'cow texture (2).png'
cow.shader = basic_lighting_shader
cow.double_sided = True
cow.turnSpeed = 1
cow.position = (0, 0.5, 10)
cow.speed = 3
cow.collider = 'cow_walk_1'

# AI logic for the cow to follow the player
def cow_update():
    if distance(cow.position, player.position) > 2:
        direction = (player.position - cow.position).normalized()
        cow.position += direction * time.dt * cow.speed

cow_update()



def cow_ai_update():
    direction = (player.position - cow.position).normalized()
    cow.position += direction * time.dt * cow.speed
    cow.lookAt(player)
    cow.rotation =  Vec3(0,cow.rotation_y + 180,0)