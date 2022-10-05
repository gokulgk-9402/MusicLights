import socket
import threading
import time
from rpi_ws281x import *

HEADER = 64
SERVER = "192.168.1.204"
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DC_MSG = "!DC"

LED_COUNT = 60
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 100
LED_INVERT = False
LED_CHANNEL = 0


strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


mem = {
    1: [29],
    2: [28, 30, 40, 41, 17, 18],
    3: [27, 31, 42, 39, 16, 19, 7, 5, 6, 51, 52, 53],
    4: [26, 32, 43, 38, 15, 20, 8, 4, 50, 54]
}

colors = {
    1: Color(0, 20, 20),
    2: Color(0, 20, 0),
    3: Color(20, 20, 0),
    4: Color(20, 0, 0)
}

decibels = {
    1: -25,
    2: -20,
    3: -13,
    4: -10,
}

def handle_client(conn, addr):
    print(f"Client - {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        message = conn.recv(msg_length).decode(FORMAT)
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        if message == DC_MSG:
            connected = False
            print(f"{addr} Disconnected!")
        else:
            # print(f"{addr}: {message}")
            db = float(message.split()[-1])
            for i in range(1, 5):
                if db > decibels[i]:
                    for led in mem[i]:
                        strip.setPixelColor(led, colors[i])
                    strip.show()
            # strip.show()

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
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(50, 50, 50))
    strip.show()
    time.sleep(0.5)
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0, 0, 0))
    strip.show()
    start()
