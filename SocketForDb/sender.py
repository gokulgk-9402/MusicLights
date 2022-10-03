import socket
import time
import pyaudio
from math import log10
import audioop

p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 0
print(p.get_default_input_device_info())

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

def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue

if __name__ == "__main__":
    stream = p.open(format=p.get_format_from_width(WIDTH),
                input_device_index=DEVICE,
                channels=1,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=callback)

    stream.start_stream()

    prev = 0
    iteration = 0
    while stream.is_active(): 
        if rms != 0:
            db = 20 * log10(rms)
            # print(f"RMS: {rms} DB: {db}") 
            # refresh every 0.3 seconds 
            # if db - prev > 5 or db > -10:
            #     # print(db)
            #     # print(db)
            #     # print("."*int(db+60))
            #     send(f"!DB {db}")
            # else:
            #     if iteration % 20 == 0:
            #         iteration = 0
                    # print(" ")
            prev = db
            # iteration += 1
            send(f"!DB {db * 0.6}")
            time.sleep(0.01)

    stream.stop_stream()
    stream.close()

    p.terminate()
    # while True:
    #     message = input("Enter message to send: ")
    #     send(message)
    #     if message == DC_MSG:
    #         break
