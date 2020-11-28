import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
FORMAT = "UTF-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

subscription_dict = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    d = {conn : '0'}
    subscription_dict.update(d)
    print(subscription_dict) 
    connected = True
    while connected:
        topic_len = conn.recv(HEADER).decode(FORMAT)
        if topic_len:
            topic_len = int(topic_len)
            msg = conn.recv(topic_len).decode(FORMAT)
            payload_len = conn.recv(HEADER).decode(FORMAT)
            if payload_len:
                payload_len = int(payload_len)
                payload = conn.recv(payload_len).decode(FORMAT)
            if (payload == DISCONNECT_MESSAGE):
                connected = False
            print(f"[{addr}] {msg} : {payload}")
            #conn.send("Msg recieved".encode(FORMAT))
    conn.close()

def start():
    server.listen()
    print (f"[LISTENING] Server is listening on: {SERVER}")
    while True:
        conn, addr = server.accept()
        thread= threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


print ("[STARTING] server is starting...")
start()