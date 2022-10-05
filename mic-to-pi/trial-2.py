import pyaudio
import time
from math import log10
import audioop  
from rpi_ws281x import *


LED_COUNT = 60
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 100
LED_INVERT = False
LED_CHANNEL = 0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

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


p = pyaudio.PyAudio()
WIDTH = 2
RATE = int(p.get_default_input_device_info()['defaultSampleRate'])
DEVICE = p.get_default_input_device_info()['index']
rms = 0
print(p.get_default_input_device_info())

def callback(in_data, frame_count, time_info, status):
    global rms
    rms = audioop.rms(in_data, WIDTH) / 32767
    return in_data, pyaudio.paContinue


stream = p.open(format=p.get_format_from_width(WIDTH),
                input_device_index=DEVICE,
                channels=1,
                rate=RATE,
                input=True,
                output=False,
                stream_callback=callback)

stream.start_stream()

while stream.is_active(): 
    if rms > 0:
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        db = 20 * log10(rms)
        if db > -30:
            for i in range(12):
                strip.setPixelColor(i, Color(0, 20, 20))
        if db > -25:
            for i in range(13, 24):
                strip.setPixelColor(i, Color(0, 20, 0))
        if db > -20:
            for i in range(25, 36):
                strip.setPixelColor(i, Color(20, 20, 0))
        if db > -16:
            for i in range(37, 48):
                strip.setPixelColor(i, Color(20, 8, 0))
        if db > -13:
            for i in range(48, 60):
                strip.setPixelColor(i, Color(20, 0, 0))

        strip.show()

    time.sleep(0.05)

stream.stop_stream()
stream.close()

p.terminate()
