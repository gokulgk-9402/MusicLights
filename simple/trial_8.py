from rpi_ws281x import *
import time
import random

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
    3: [27, 31, 42, 39, 16, 19, 7, 5, 6, 51, 52, 53]
}

colors = {
    1: Color(100, 0, 0),
    2: Color(100, 50, 0),
    3: Color(100, 100, 0)
}

while True:
    for i in range(1, 4):
        for led in mem[i]:
            strip.setPixelColor(led, colors[i])
        strip.show()
        time.sleep(0.1)
    
    for i in range(3, 0, -1):
        for led in mem[i]:
            strip.setPixelColor(led, Color(0, 0, 0))
        strip.show()
        time.sleep(0.1)