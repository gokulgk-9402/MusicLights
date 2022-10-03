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

while True:
    tolight = int(input('Enter LED ID: '))
    strip.setPixelColor(tolight, Color(100, 100, 100))
    strip.show()
    time.sleep(2)
    strip.setPixelColor(tolight, Color(0, 0, 0))
    strip.show()
    time.sleep(0.5)