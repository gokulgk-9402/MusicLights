# Audio Responsive Lights with Raspberry Pi

## Componenets used:
* [Raspberry Pi 4B](https://www.amazon.in/gp/product/B07XSJ64ZY/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
* [WS2812B LED strip](https://www.amazon.in/gp/product/B0B4KZ7HRG/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)(1 metre, 60 LEDs)
* BreadBoard
* Jumper Wires
* Bottle
## Idea:
My idea is to make the LEDs in a WS2812B LED strip (60 LEDs, 1 metre in length) respond to the sound around it (songs, music, etc.). I used Raspberry Pi 4 to control the LED strip. I have taped the LED strip around a bottle, 12 LED's per row and 5 rows. I want to explore different patterns that I can create using the LED strip. And I would like to fine tune the decibel/sound intensity values for which a change in lighting would be pleasant. This is a project that will get better with time, so here are my notes for it, I'll mention it here whenever a change is made. 

## Notes:

#### September 28, 2022
Trial one of using LED strip with pi. There were some troubles I ran into while soldering, but finally the soldering was done. And I tried out some simple patterns I tested out coding for. They are inside the folder `simple` in the repo.
#### September 29, 2022
Tested out using pyaudio to record sound intensity. Came out to be good. Tried some more simple patterns with the light strip. 
#### October 1, 2022
I came to know that the 3.5mm jack in Raspberry pi is only for input and not for output. So for now I have settled with using laptop for recording sound intensity values and sending it to my pi through socket programming. The pi is the server and my laptop is the client. As of right now they are in the same network and their IP addresses are hard coded, which could be improved in the future. When I get an USB mic for pi, this socket programming part can be avoided. 
The decibel values for which the light has to responded can be fine tuned in the server side program (the one that runs in the PI) or the decibel values can be changed in the laptop and sent to the pi. Instead of decibel, the rms values that pyaudio calculates can also be used to make the lights respond in a different way. 
One of the sample results is there in the repo. It was my light's response to the song [Shape Of You](https://www.youtube.com/watch?v=JGwWNGJdvx8) by Ed Sheeran. *This is a sample footage, and only 10 seconds.* 
Download [this video](https://github.com/gokulgk-9402/MusicLights/blob/main/SampleVids/pattern2_Shape_Of_You.mp4) to see the lights reacting with sound.

![](https://github.com/gokulgk-9402/MusicLights/blob/main/SampleVids/pattern2_Shape_Of_You.gif)

#### October 3, 2022
Today, I tried creating newer patterns. Tried making letters, but it was quite difficult. But I have written a program to turn on LED's one by one, so I know which numbered LED is needed for which pattern/letter I am planning to use. This can be improved in the future with an on/off argument. And I have written a code for a hexagonal pattern which can be used in the future for another way to visualize the sound.

#### October 5, 2022
Got the USB mic for Raspberry Pi, so now I don't need to use socket programming to send decibel values to pi, instead record decibel values using that itself and control the lights. Also now I can use [pm2](https://pm2.keymetrics.io/) to make my code run indefinitely and run it automatically on startup of the pi. The codes inside the folder `mic-to-pi` are for that direct use of mic with pi. 


#### October 8, 2022
Added a 8x8 LED matrix display to display key changes and a welcome message. Started working on mobile app with kivy for this but it kept crashing when I tried to run in android. Then tried a simpler application which required me to send a "command version" of the changes in status, brightness, sensitivity of the lights.

#### October 12, 2022
After many attempts at making the app, finally it worked out. I tred using adb to check the application logs, but yeah it was like looking for needle in a haystack and gave up. I added widgets to the application one by one and made minor changes each version to version. In the version `2.6` everything was almsot accourding to my plan with a few bugs and an image at the first screen missing. So, I went ahead and made version 2.7 with these changes.


The apk of this application is there in this repository - `musiclights-v2.7.apk`. Only the final version's apk is included in this repository. 

For now this project is over. Ofcourse there are improvements that are possible like improving application UI, better implementation of sensitivity, brightness, etc. But for now the basic function of the project is complete.

Also for now, this application works only when the pi is in the same local network and the IP address of the pi is fixed as the pi itself is acting as a server and mobile the client. But this can be improved if the server runs in cloud and both pi and the mobile are clients to that server. And whatever mobile client sends can be sent by the server to the pi and the pi can execute the commands. 

Sample video [here](https://youtu.be/-N7nFq8CpDo) .

#### October 20, 2022
Tried to add sliders in place of text fields for brightness and sensitivity. It was wokring fine in laptop, but when I made it into apk, it kept crashing as soon as it went to screen 2. I'm not able to figure out why. Screenshots of final version of app in folder `final-ss`. And the code of the final version is `app-v3`. 


For queries, suggestions or anything feel free to contact me:  
Discord: gk#0633  
[Instagram](https://www.instagram.com/me_is_gokul/?hl=en)  