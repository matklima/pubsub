import socket

HEADER = 64
PORT = 5050
FORMAT = "UTF-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)
TOPIC_NAME = "test topic"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send_id(id):
    send_id_data = str(id).encode(FORMAT)
    client.send(send_id_data)

def send(msg):
    payload = msg.encode(FORMAT)
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(payload)
    print(client.recv(2048).decode(FORMAT))

def subscribe(topic_name):
    send_id(1)
    payload = topic_name.encode(FORMAT)
    msg_length = len(topic_name)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(payload)
    print(client.recv(2048).decode(FORMAT))


subscribe(TOPIC_NAME)
