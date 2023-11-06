import socket
import threading
import argparse
import signal
import json
import sys
from types import SimpleNamespace

PEERS_FILE = "peers.json"

class Peer:
    def __init__(self, name, host, port, password):
        self.name = name
        self.host = host
        self.port = int(port)
        self.password = password

    def send_message(self, recipient=None, message=None):
        try:
            peers = load_peers_from_file()
            if recipient is not None and recipient in peers:
                peer = SimpleNamespace(**peers[recipient])
                with self.create_socket_connection(peer) as s:
                    if s:
                        s.sendall(self.encode_message(self.name, message).encode('utf-8'))
            else:
                # Broadcast to all peers except the sender
                for peer_name, peer_info in peers.items():
                    if peer_name != self.name and peer_info["status"]:
                        peer = SimpleNamespace(**peer_info)
                        with self.create_socket_connection(peer) as s:
                            if s:
                                print(f"Send to peer: {peer.name}")
                                s.sendall(self.encode_message(self.name, message).encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {str(e)}")

    def receive_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((self.host, self.port))
                s.listen()
                print(f"{self.name} is listening on {self.host}:{self.port}")
                while True:
                    conn, addr = s.accept()
                    threading.Thread(target=self.handle_connection, args=(conn,)).start()
            except Exception as e:
                print(f"Error in receive_message: {str(e)}")

    def handle_connection(self, conn):
        with conn:
            data = conn.recv(1024).decode('utf-8')
            decoded_message = self.decode_message(data)
            name = decoded_message[0]
            received_message = decoded_message[1]
            print(f"{self.name} received a message from {name}: {received_message}")

  
    @staticmethod
    def create_socket_connection(peer):
        if peer:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((peer.host, peer.port))
                return s
            except Exception as e:
                print(f"Error connecting to {peer.name}: {str(e)}")
                return None
        return None

    @staticmethod
    def encode_message(name, message):
        return f"{name}-----{message}"

    @staticmethod
    def decode_message(message):
        return message.split("-----")

def save_peers_to_file(peers):
    with open(PEERS_FILE, 'w+') as file:
        json.dump(peers, file)

def save_peers_on_exit(peer=None):
    print("Saving peers before exiting...")
    peers = load_peers_from_file()
    peers[peer.name]["status"] = False
    save_peers_to_file(peers=peers)
    print(f"Updated status for {peer.name}")
    sys.exit(0)

def load_peers_from_file():
    try:
        with open(PEERS_FILE, 'r') as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def main():
    parser = argparse.ArgumentParser(description='This is a test program for demo peer-to-peer.')
    parser.add_argument('-n', '--name', help='Specify a name client.', default='test')
    parser.add_argument('-p', '--port', help='Specify a port.', default='5000')
    parser.add_argument('-ip', '--ip_addr', default='127.0.0.1', help='Specify an IP address.')
    parser.add_argument('-pw', '--password', help='Specify a password.', default='test')

    args = parser.parse_args()

    ip, port, name, password = args.ip_addr, args.port, args.name, args.password

    print("Starting for client:")
    print(f'Name: {name}')
    print(f'IP: {ip}')
    print(f'Port: {port}')

    peer = Peer(name, ip, port, password)
    peers = load_peers_from_file()

    if peer.name not in peers:
        peers[peer.name] = vars(peer)

    if peer.password != peers[name]["password"]:
        print(f"User {name} exists, but the password is incorrect!")
        print("Please try again!")
    else:
        peers[peer.name]["status"] = True
        save_peers_to_file(peers)
        signal.signal(signal.SIGINT, lambda signum, frame: save_peers_on_exit(peer=peer))
        signal.signal(signal.SIGTSTP, lambda signum, frame: save_peers_on_exit(peer=peer))
        threading.Thread(target=peer.receive_message).start()
        peer.send_message(message=f"{peer.name} has joined the chat!")
        message = ""

        while True:
            person = input("Who do you want to chat:")
            if person and person != "all":
                message = input("Please enter 'exit' to leave chat/enter message:")
                peer.send_message(recipient=person, message=message)
            else:
                message = input("Please enter 'exit' to leave chat/enter message:")
                peer.send_message(message=message)

            if message.lower() == "exit":
                save_peers_on_exit(peer=peer)
                break

if __name__ == "__main__":
    main()
