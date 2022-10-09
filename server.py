import socket
import threading
import time
import json
import os

HEADER = 64
SERVER = "192.168.1.204"
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DC_MSG = "!DC"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"Client - {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        message = conn.recv(msg_length).decode(FORMAT)

        if message == DC_MSG:
            connected = False
            print(f"{addr} Disconnected!")
        else:
            # print(f"{addr}: {message}")
            cmd,data = message.split()
            print(cmd, data)
            
            f = open('data.json')
            d = json.load(f)
            f.close()
            print(d)
            if cmd == '!sens':
                d['sens'] = float(data)
            elif cmd == '!bright':
                d['brightness'] = int(float(data))
            elif cmd == '!status':
                d['status'] = data
            print(d)
            with open('data.json', 'w') as file:
                json.dump(d,file)
            time.sleep(0.2)

            os.system("sudo pm2 restart LED")

    conn.close()

def start():
    server.listen()
    while True:
        print("Waiting for connection...")
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args = (conn, addr))
        print(f"Active connections: {threading.active_count() - 1}")
        thread.start()

if __name__ == "__main__":

    print("Server is starting....")
    start()
