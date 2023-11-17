from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading
import socket

app = Flask(__name__)
socketio = SocketIO(app)

# Chat server code (similar to what you provided)
host = '0.0.0.0'
port = 55555
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

print(f"Server listening on {host}:{port}")

clients = []

def handle_client(client_socket, addr):
    # Broadcast a welcome message to the connected client
    client_socket.send("Welcome to the chat room!\n".encode('utf-8'))

    # Notify other clients about the new connection
    broadcast(f"{addr} has joined the chat.\n", client_socket)

    # Receive and broadcast messages
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            broadcast(f"{addr}: {message}", client_socket)
        except Exception as e:
            print(e)
            break

    # Remove the client from the list and notify others
    clients.remove(client_socket)
    broadcast(f"{addr} has left the chat.\n", client_socket)

def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(e)
                clients.remove(client)

def start_chat_server():
    while True:
        client_socket, addr = server_socket.accept()
        clients.append(client_socket)

        client_thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_thread.start()

# Start the chat server in a separate thread
chat_server_thread = threading.Thread(target=start_chat_server)
chat_server_thread.start()

# Flask routes and socket events
@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    emit('message', message, broadcast=True)

if __name__ == '__main__':
    socketio.run(app,host=host,port=8888)
