# server.py
import socket
import threading
import pickle

# Server setup
SERVER = 'localhost'
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))
server.listen()

clients = []
game_state = {"players": {}}

def broadcast(data, sender_conn):
    for client in clients:
        if client != sender_conn:
            client.send(data)

def handle_client(conn, addr):
    print(f"New connection: {addr}")
    clients.append(conn)
    
    while True:
        try:
            data = conn.recv(4096)
            if data:
                received_data = pickle.loads(data)
                if received_data["type"] == "position":
                    game_state["players"][addr] = received_data["data"]
                broadcast(data, conn)
        except Exception as e:
            print(f"Error handling client {addr}: {str(e)}")
            clients.remove(conn)
            conn.close()
            break

    print(f"Connection closed: {addr}")

print(f"Server started on {SERVER}:{PORT}")
while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()
    print(f"Active connections: {threading.activeCount() - 1}")


