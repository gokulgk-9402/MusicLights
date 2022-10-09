import socket
import time

HEADER = 64
SERVER = "192.168.1.204"
PORT = 5050
FORMAT = 'utf-8'
DC_MSG = "!DC"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)

if __name__ == "__main__":
    to = input("Enter on/off: ")
    send(f"!SWITCH {to}")
    send(DC_MSG)