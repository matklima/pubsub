import socket
import threading

HEADER = 64
PORT = 5050
FORMAT = "UTF-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def send_id(id):
    send_id_data = str(id).encode(FORMAT)
    client.send(send_id_data)

def check_response():
    connected = True
    while connected:
        lock.acquire()
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
        lock.release()


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

def send(topic_name, msg):
    send_id(0)

    payload = msg.encode(FORMAT)
    #prepare message length to send
    msg_length = len(msg)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))

    #prepare topic length to send
    topic_length = len(topic_name)
    send_t_length = str(topic_length).encode(FORMAT)
    send_t_length += b' ' * (HEADER - len(send_t_length))
    send_topic_name = str(topic_name).encode(FORMAT)

    client.send(send_t_length)
    client.send(send_topic_name)

    client.send(send_length)
    client.send(payload)
    print(f"[{client}] {send_topic_name} : {payload}")

def unsubscribe(topic_name):
    send_id(2)
    payload = topic_name.encode(FORMAT)
    msg_length = len(topic_name)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(payload)

def start():
    print ("What do you want to do? (possible options: connect, subscribe, publish, disconnect, unsubscribe, help")
    connected = False
    have_job = True
    while have_job:
        value = input()

        if value == "connect":
            client.connect(ADDR)
            connected = True
        elif value == "publish":
            topic_to_publish_to = input("Enter topic you want to publish to:")
            if connected == True:
                message_to_publish = input("Enter message to publish: \n")
                send(topic_to_publish_to, message_to_publish)
            else:
                print("No connection active")
        elif value == "subscribe":
            if connected == True:
                topic_name = input("Enter topic name to subscribe to: \n")
                subscribe(topic_name)
            else:
                print("No connection active")
        elif value == "unsubscribe":
            if connected == True:
                topic_name = input("Enter topic name to subscribe to: \n")
                unsubscribe(topic_name)
            else:
                print("No connection active")
        elif value == "disconnect":
            if connected == True:
                send(topic_name, DISCONNECT_MESSAGE)
                have_job = False
            else:
                print("No connection active")
        else:
            print("No option available")

lock = threading.Lock()  
start()
# send("Hello World!")
# input()
# send("Hello Mateo!")
# input()
# send("Hello another time!")
# input()
# send(DISCONNECT_MESSAGE)