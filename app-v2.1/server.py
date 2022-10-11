import socket
import threading
import time
import json
import os

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


HEADER = 64
SERVER = "192.168.1.204"
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DC_MSG = "!DC"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1, block_orientation=0,
                    rotate=1, blocks_arranged_in_reverse_order=False)
print("Created device")

def matrix_show(msg, font=LCD_FONT):
# print(msg)
    show_message(device, msg, fill="white", font=proportional(font), scroll_delay=0.05)

# os.system("sudo python matrix.py")

def handle_client(conn, addr):
    print(f"Client - {addr} connected.")
    # matrix_show("Application connected!")
    matrix_show(':)', CP437_FONT)

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        message = conn.recv(msg_length).decode(FORMAT)

        if message == DC_MSG:
            connected = False
            print(f"{addr} Disconnected!")
            # matrix_show("Application disconnected!")
            matrix_show(":(")
        else:
            # print(f"{addr}: {message}")
            cmd,data = message.split()
            print(cmd, data)
            
            f = open('data.json')
            d = json.load(f)
            f.close()
            # print(d)
            if cmd == '!cur':
                print(cmd, cmd, d[data])
                send_msg(conn, f'{d[data]}')
                
            elif cmd == '!sens':
                d['sens'] = float(data)
                with open('data.json', 'w') as file:
                    json.dump(d,file)
                # matrix_show(f"Sensitivity set to {d['sens']}.")
                matrix_show(f"Sens: {d['sens']}")
                os.system("sudo pm2 restart LED")
            elif cmd == '!bright':
                d['brightness'] = int(float(data))
                with open('data.json', 'w') as file:
                    json.dump(d,file)
                # matrix_show(f"Brightness set to {d['brightness']}.")
                matrix_show(f"Brightness: {d['brightness']}")
                os.system("sudo pm2 restart LED")
            elif cmd == '!status':
                d['status'] = data
                with open('data.json', 'w') as file:
                    json.dump(d,file)
                if data != 'on':
                    os.system("sudo pm2 stop LED")
                    os.system("sudo python off.py")
                    # matrix_show("Status set to Off.")
                    matrix_show("Off!")
                else:
                    # matrix_show("Status set to On.")
                    os.system("sudo pm2 restart LED")
                    matrix_show("On!!!")
            # print(d)
            # with open('data.json', 'w') as file:
            #     json.dump(d,file)
            # time.sleep(0.2)

            

    conn.close()

def send_msg(conn, message):
    msg = message.encode('utf-8')
    msg_len = len(msg)
    send_len = str(msg_len).encode('utf-8')
    send_len += b' ' * (64 - len(send_len))
    conn.send(send_len)
    conn.send(msg)


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
    matrix_show("Hi Gokul!")
    start()
