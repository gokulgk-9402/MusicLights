from rpi_ws281x import *
import time
import random

LED_COUNT = 60
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

for t in range(10):
	for i in range(LED_COUNT):
		strip.setPixelColor(i, Color(i*10, 0, i*20))
		strip.setPixelColor(LED_COUNT - i, Color(i*20, 0, i*10))
		strip.show()
		time.sleep(0.1)
		strip.setPixelColor(i, Color(0, 0, 0))
		strip.setPixelColor(LED_COUNT - i, Color(0, 0, 0))

strip.show()
