# Audio Responsive Lights with Raspberry Pi

## Componenets used:

### Notes:
#### Idea:
My idea is to make the LEDs in a WS2812B LED strip (60 LEDs, 1 metre in length) respond to the sound around it (songs, music, etc.). I used Raspberry Pi 4 to control the LED strip. I have taped the LED strip around a bottle, 12 LED's per row and 5 rows. I want to explore different patterns that I can create using the LED strip. And I would like to fine tune the decibel/sound intensity values for which a change in lighting would be pleasant. This is a project that will get better with time, so here are my notes for it, I'll mention it here whenever a change is made. 
#### September 28, 2022
Trial one of using LED strip with pi. There were some troubles I ran into while soldering, but finally the soldering was done. And I tried out some simple patterns I tested out coding for. They are inside the folder `simple` in the repo.
#### September 29, 2022
Tested out using pyaudio to record sound intensity. Came out to be good. Tried some more simple patterns with the light strip. 
#### October 1, 2022
I came to know that the 3.5mm jack in Raspberry pi is only for input and not for output. So for now I have settled with using laptop for recording sound intensity values and sending it to my pi through socket programming. The pi is the server and my laptop is the client. As of right now they are in the same network and their IP addresses are hard coded, which could be improved in the future. When I get an USB mic for pi, this socket programming part can be avoided. 
The decibel values for which the light has to responded can be fine tuned in the server side program (the one that runs in the PI) or the decibel values can be changed in the laptop and sent to the pi. Instead of decibel, the rms values that pyaudio calculates can also be used to make the lights respond in a different way. 
One of the sample results is there in the repo. It was my light's response to the song [Shape Of You](https://www.youtube.com/watch?v=JGwWNGJdvx8) by Ed Sheeran. **This is a sample footage, and only 10 seconds.**

![](https://github.com/gokulgk-9402/MusicLights/blob/main/SampleVids/pattern2_Shape_Of_You.gif)