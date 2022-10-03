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

for i in range(30):
        for i in range(6, LED_COUNT, 12):
                strip.setPixelColor(i, Color(0, 255, 0))
                # strip.setPixelColor(i, Color(0, 255, 0))
        strip.show()
        time.sleep(0.05)

        for i in range(6, LED_COUNT, 12):
                strip.setPixelColor(i-1, Color(200, 200, 0))
                strip.setPixelColor(i+1, Color(200, 200, 0))
        strip.show()
        time.sleep(0.05)

        for i in range(6, LED_COUNT, 12):
                strip.setPixelColor(i-2, Color(150, 96, 0))
                strip.setPixelColor(i+2, Color(150, 96, 0))
        strip.show()
        time.sleep(0.1)

        for i in range(6, LED_COUNT, 12):
                strip.setPixelColor(i+3, Color(100, 0, 0))
                strip.setPixelColor(i-3, Color(100, 0, 0))
        strip.show()
        time.sleep(0.1)

        for i in range(6, LED_COUNT, 12):
                strip.setPixelColor(i-3, Color(0, 0, 0))
                strip.setPixelColor(i+3, Color(0, 0, 0))
        strip.show()
        time.sleep(0.1)

        for i in range(6, LED_COUNT, 12):
                strip.setPixelColor(i-2, Color(0, 0, 0))
                strip.setPixelColor(i+2, Color(0, 0, 0))
        strip.show()
        time.sleep(0.05)

        for i in range(6, LED_COUNT, 12):
                strip.setPixelColor(i-1, Color(0, 0, 0))
                strip.setPixelColor(i+1, Color(0, 0, 0))
        strip.show()
        time.sleep(0.05)

        for i in range(6, LED_COUNT, 12):
                strip.setPixelColor(i, Color(0, 0, 0))
                strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(0.5)

for i in range(6, LED_COUNT, 12):
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.setPixelColor(i, Color(0, 0, 0))

strip.show()
