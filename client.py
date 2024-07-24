from ursina import *
import random
import socket
import threading
import pickle
from ursina.prefabs.first_person_controller import FirstPersonController

# Client setup
SERVER = 'localhost'
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((SERVER, PORT))
except socket.error as e:
    print(str(e))

def receive_data():
    while True:
        try:
            data = client.recv(4096)
            if data:
                received_data = pickle.loads(data)
                if received_data["type"] == "position":
                    addr = received_data["addr"]
                    if addr not in players:
                        players[addr] = Entity(model='cube', color=color.random_color(), position=received_data["data"])
                    else:
                        players[addr].position = received_data["data"]
        except Exception as e:
            print(str(e))
            break

def send_data(data):
    try:
        serialized_data = pickle.dumps(data)
        client.send(serialized_data)
    except socket.error as e:
        print(str(e))

receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

# Ursina game setup
app = Ursina()

render_distance = 10

for z in range(render_distance):
    for x in range(render_distance):
        Entity(
            model="cube", color=color.green, collider="box", ignore=True,
            position=(x, 0, z),
            parent=scene,
            origin_y=0.5,
            texture="download (8).jpeg",
        )

for z in range(render_distance):
    for x in range(render_distance):
        Entity(
            model="cube", color=color.gray, collider="box", ignore=True,
            position=(x, -1, z),
            parent=scene,
            origin_y=0.5,
            texture='download (9).jpeg',
        )

for z in range(render_distance):
    for x in range(render_distance):
        Entity(
            model="cube", color=color.gray, collider="box", ignore=True,
            position=(x, -2, z),
            parent=scene,
            origin_y=0.5,
            texture="download (9).jpeg",
        )

for z in range(render_distance):
    for x in range(render_distance):
        Entity(
            model="cube", collider="box", ignore=True,
            position=(x, -3, z),
            parent=scene,
            origin_y=0.5,
            texture="download.png",
        )

players = {}
player = FirstPersonController(model = 'cube ',texture ='wood texture.png')
players["me"] = player

def update():
    send_data({"type": "position", "addr": "me", "data": player.position})

skybox_image = load_texture("download (11).jpeg")
Sky(texture=skybox_image)

Audio(sound_file_name='08 - Minecraft.mp3', volume=1, pitch=1, balance=0, loop=True, loops=1, autoplay=True, auto_destroy=False)

app.run()
