import wave
from pathlib import Path
import simpleaudio
import argparse
from nltk.corpus import cmudict
import re
import struct
import numpy as np

audio = []
sample_rate = 16000

num_samples = 1000 * (sample_rate / 1000.0)

for x in range(int(num_samples)):
    audio.append(0)

wav_file=wave.open('test.wav',"w")

nchannels = 1

sampwidth = 2

nframes = len(audio)
comptype = "NONE"
compname = "not compressed"
wav_file.setparams((nchannels, sampwidth, sample_rate, nframes, comptype, compname))

# for sample in audio:
#     wav_file.writeframes(struct.pack('h', int( sample * 0)))#32767.0

wav_file.writeframes(struct.pack('h'*len(audio), *audio))

wav_file.close()

f = wave.open('test.wav',"r")
time_count = f.getparams().nframes/f.getparams().framerate
print(time_count)
f.close()

f = wave.open('new.wav','r')
p = f.getparams()
print(p)
nframes = f.getnframes()
diphone_data = f.readframes(nframes)
temp = np.frombuffer(diphone_data, np.int16)
print(temp)
print(type(temp))
print(len(temp))
time_count = f.getparams().nframes/f.getparams().framerate
print(time_count)
f.close()