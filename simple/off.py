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

for x in range(LED_COUNT):
	strip.setPixelColor(x, Color(0, 0, 0))

#for i in range(5):
 #       for x in range(0, LED_COUNT - 2, 3):
  #              v1 = random.randrange(0, 255)
   #             v2 = random.randrange(0, 255)
    #            v3 = random.randrange(0, 255)
     #           print(v1, v2, v3)
      #          strip.setPixelColor(x, Color(v1, v2, v3))
       #         strip.setPixelColor(x+1, Color(v1%20, v2%20, v2%20))
        #        strip.setPixelColor(x+2, Color(v1%5, v2%5, v3%5))
         #       strip.show()
          #      time.sleep(2)
           #     strip.setPixelColor(x, Color(0, 0, 0))
            #    strip.setPixelColor(x+1, Color(0, 0, 0))
             #   strip.setPixelColor(x+2, Color(0, 0, 0))

strip.show()
