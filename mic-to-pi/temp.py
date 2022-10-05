import pyaudio
import time
from math import log10
import audioop  

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
		db = 20 * log10(rms)
		if db > -10:
			print("-10 reached!")
		elif db > -20:
			print("-20 reached!")
		elif db > -30:
			print("-30 reached!")
		# print(f"RMS: {rms} DB: {db}") 
	else:
		print(0)
    # refresh every 0.3 seconds 
	time.sleep(0.01)
	

stream.stop_stream()
stream.close()

p.terminate()
