import socket
import threading

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


def check_response():
    connected = True
    while connected:
        topic_len = client.recv(HEADER).decode(FORMAT)
        if topic_len:
            topic_len = int(topic_len)
            msg = client.recv(topic_len).decode(FORMAT)
            payload_len = client.recv(HEADER).decode(FORMAT)
            if payload_len:
                payload_len = int(payload_len)
                payload = client.recv(payload_len).decode(FORMAT)
            print(f"[SERVER:] {msg} : {payload}")
            if (payload == DISCONNECT_MESSAGE):
                    connected = False

def subscribe(topic_name):
    send_id(1)
    payload = topic_name.encode(FORMAT)
    msg_length = len(topic_name)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(payload)
    thread= threading.Thread(target=check_response)
    thread.start()

subscribe(TOPIC_NAME)
