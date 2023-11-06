import socket
import threading
import argparse
import signal
PEERS_FILE = "peers.json"
import json
import sys
from types import SimpleNamespace

class Peer:
    def __init__(self, name, host, port, password):
        self.name = name
        self.host = host
        self.port = int(port)
        self.password = password

    def send_message(self, recipient=None, peers=None, message=None):
        try:
            if recipient is not None:
                peer = SimpleNamespace(**peers[recipient])
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((peer.host, peer.port))
                        s.sendall(self.encode_message(self.name, message).encode('utf-8'))
                except Exception as e:
                            print(f"Error sending message to {peer.name}: {str(e)}")
            else:
                # Broadcast to all peers except the sender
                for peer_name, peer_info in peers.items():
                    if peer_name != self.name and peer_info["status"]:
                        try:
                            peer = SimpleNamespace(**peer_info)
                            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                                s.connect((peer.host, peer.port))
                                s.sendall(self.encode_message(self.name, message).encode('utf-8'))
                        except Exception as e:
                            print(f"Error sending message to {peer_name}: {str(e)}")
        except Exception as e:
            print(f"Error: {str(e)}")


    def receive_message(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f"{self.name} is listening on {self.host}:{self.port}")
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_connection, args=(conn,)).start()

    def handle_connection(self, conn):
        with conn:
            data = conn.recv(1024).decode('utf-8')
            decode_mess = self.decode_message(data)
            name = decode_mess[0]
            message = decode_mess[1]
            print(f"{self.name} received a message from {name}: {message}")

    def encode_message(self, name, message):
        return f"{name}-----{message}"

    def decode_message(self, message):
        return message.split("-----")
    
def save_peers_to_file(peers):
    with open(PEERS_FILE, 'w+') as file:
        json.dump(peers, file)


def save_peers_on_exit(peers=None, peer=None):
    print("Saving peers before exiting...")
    peers[peer.name]["status"] = False
    save_peers_to_file(peers=peers)
    print(f"Update status for {peer.name}")
    sys.exit(0)

def load_peers_from_file():
    try:
        with open(PEERS_FILE, 'r') as file:
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def main():
    parser = argparse.ArgumentParser(description='This is test programe for demo peer to peer.')
    # parser.add_argument('-n', '--name', help='Specify a name client.', required=True)
    # parser.add_argument('-p', '--port', help='Specify a port.', required=True)
    # parser.add_argument('-ip', '--ip_addr', default='127.0.0.1', help='Specify a ip address.')
    # parser.add_argument('-pw', '--password', help='Specify a password.', required = True)

    parser.add_argument('-n', '--name', help='Specify a name client.', default='test')
    parser.add_argument('-p', '--port', help='Specify a port.', default='5000')
    parser.add_argument('-ip', '--ip_addr', default='127.0.0.1', help='Specify a ip address.')
    parser.add_argument('-pw', '--password', help='Specify a password.', default='test')

    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the values of the arguments
    ip = args.ip_addr
    port = args.port
    name = args.name
    password = args.password
    return name, ip, port, password

if __name__ =="__main__":
    name, ip, port, password = main()
    # Your program logic goes here
    print("Starting for client:")
    print(f'Name: {name}')
    print(f'IP: {ip}')
    print(f'Port: {port}')
    peer = Peer(name, ip, port, password)
     # Register the signal handler
    peers = load_peers_from_file()
    if peer.name not in peers:
        peers[peer.name] = vars(peer)
    if peer.password  != peers[name]["password"]:
        print(f"User {name} have exist, but password not exactly!")
        print(f"Please try again!")
    else:
         # Register the signal handlers
        peers[peer.name]["status"] = True
        save_peers_to_file(peers)
        signal.signal(signal.SIGINT, lambda signum, frame: save_peers_on_exit(peer=peer, peers=peers))
        signal.signal(signal.SIGTSTP, lambda signum, frame: save_peers_on_exit(peer=peer, peers=peers))
        threading.Thread(target=peer.receive_message).start()
        peer.send_message(peers=peers, message=f"{peer.name} has joint chat!")
        message=""
        while True:
            person = input("who do you want to chat:")
            if person != None and person != "" and person != "all":
                message = input("Please enter exit to leave chat/enter message:")
                peer.send_message(recipient=person,peers=peers, message=message)
            else:
                message = input("Please enter exit to leave chat/enter message:")
                peer.send_message(peers=peers, message=message)
            if message.lower() == "exit":
                break
