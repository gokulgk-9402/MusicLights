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
            if db > -40:
                for i in range(12):
                    strip.setPixelColor(i, Color(0, 20, 20))
            if db > -30:
                for i in range(13, 24):
                    strip.setPixelColor(i, Color(0, 20, 0))
            if db > -20:
                for i in range(25, 36):
                    strip.setPixelColor(i, Color(20, 20, 0))
            if db > -15:
                for i in range(37, 48):
                    strip.setPixelColor(i, Color(20, 8, 0))
            if db > -10:
                for i in range(48, 60):
                    strip.setPixelColor(i, Color(20, 0, 0))

            strip.show()

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
