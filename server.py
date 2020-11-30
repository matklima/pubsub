import socket
import threading

HEADER = 64
FORMAT = "UTF-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

subscription_dict = dict()
topic_list = set()

def send(client, topic_name, payload):
    payload = payload.encode(FORMAT)
    #prepare message length to send
    msg_length = len(payload)
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


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    d = {conn : ['0']}
    subscription_dict.update(d)
    connected = True
    while connected:
        identifier = conn.recv(1).decode(FORMAT)
        identifier_id = int(identifier)
        if identifier_id == 0:
            topic_len = conn.recv(HEADER).decode(FORMAT)
            if topic_len:
                topic_len = int(topic_len)
                msg = conn.recv(topic_len).decode(FORMAT)
                topic_list.add(str(msg))
                payload_len = conn.recv(HEADER).decode(FORMAT)
                if payload_len:
                    payload_len = int(payload_len)
                    payload = conn.recv(payload_len).decode(FORMAT)
                if (payload == DISCONNECT_MESSAGE):
                    connected = False
                print(f"[{addr}] {msg} : {payload}")
                for key, val in subscription_dict.items():
                    if msg in val:
                        send(key, msg, payload)
        elif identifier_id == 1:
            topic_len = conn.recv(HEADER).decode(FORMAT)
            if topic_len:
                topic_len = int(topic_len)
                msg = conn.recv(topic_len).decode(FORMAT)
                if msg in topic_list:
                    subscription_dict.setdefault(conn, []).append(msg)
                    print (f"Subscribed to {msg}")
                else:
                    print ("No such topic")
        elif identifier_id == 2:
            topic_len = conn.recv(HEADER).decode(FORMAT)
            if topic_len:
                topic_len = int(topic_len)
                msg = conn.recv(topic_len).decode(FORMAT)
                if msg in topic_list:
                    subscription_dict.setdefault(conn, []).remove(msg)
                    print (f"Unsubscribed from: {msg}")
                else:
                    print ("No such topic")
        elif identifier_id == 3:
            # topic_len = conn.recv(HEADER).decode(FORMAT)
            # if topic_len:
            #     topic_len = int(topic_len)
            #     msg = conn.recv(topic_len).decode(FORMAT)
            #     if msg in topic_list:
            #         subscription_dict.setdefault(conn, []).remove(msg)
            #         print (f"Disconnectiong, all nodes connected to: {msg} will be unsubscribed!")
                connected = False

        else:
            print ("wrong identifier")
            connected = False

    conn.close()

def start():
    
    run = False
    port = input("Enter port:\n")
    if port.isdigit():
        run=True
        SERVER = socket.gethostbyname(socket.getfqdn())
        ADDR = (SERVER, int(port))
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(ADDR)
        server.listen()
        print (f"[LISTENING] Server is listening on: {SERVER}")

    while run:
        conn, addr = server.accept()
        thread= threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount()-1}")


print ("[STARTING] server is starting...")
start()