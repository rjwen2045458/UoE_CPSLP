#playaudio.py

import pyaudio # on your own machines, you might need to install this to run the code contained here
import wave

CHUNK = 1024

wf = wave.open('kdt48.wav', 'rb')

p = pyaudio.PyAudio()


# By changing the samplerate we change the playback speed
# The actual samples (amplitude values) remain the same but
# are played back faster (higher samplerate) or slower (lower samplerate)
# This also changes the percieved frequency of the audio
# which will be higher or lower pitched (higher or lower samplerate respectively)


#samplerate = wf.getframerate()
#samplerate = wf.getframerate() * 2
samplerate = int(wf.getframerate() * 0.5) # remember to cast as an int

stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=samplerate,
                output=True)

data = wf.readframes(CHUNK)

while data:
    stream.write(data)
    data = wf.readframes(CHUNK)

stream.stop_stream()
stream.close()
p.terminate()