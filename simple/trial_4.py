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
        for i in range(3, LED_COUNT, 5):
                strip.setPixelColor(i, Color(0, 100, 100))
                strip.setPixelColor(i, Color(0, 100, 100))
        strip.show()
        time.sleep(0.05)

        for i in range(3, LED_COUNT, 5):
                strip.setPixelColor(i-1, Color(20, 20, 0))
                strip.setPixelColor(i+1, Color(20, 20, 0))
        strip.show()
        time.sleep(0.05)

        for i in range(3, LED_COUNT, 5):
                strip.setPixelColor(i-2, Color(10, 0, 10))
                strip.setPixelColor(i+2, Color(10, 0, 10))
        strip.show()
        time.sleep(0.1)

        for i in range(3, LED_COUNT, 5):
                strip.setPixelColor(i-2, Color(0, 0, 0))
                strip.setPixelColor(i+2, Color(0, 0, 0))
        strip.show()
        time.sleep(0.05)

        for i in range(3, LED_COUNT, 5):
                strip.setPixelColor(i-1, Color(0, 0, 0))
                strip.setPixelColor(i+1, Color(0, 0, 0))
        strip.show()
        time.sleep(0.05)

        for i in range(3, LED_COUNT, 5):
                strip.setPixelColor(i, Color(0, 0, 0))
                strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()
        time.sleep(0.5)

for i in range(3, LED_COUNT, 5):
	strip.setPixelColor(i, Color(0, 0, 0))
	strip.setPixelColor(i, Color(0, 0, 0))

strip.show()
