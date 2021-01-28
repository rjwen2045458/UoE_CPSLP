import wave
import math

nina = wave.open("nina8.wav", 'rb') # make sure wave file in available in current directory

# getsampwidth() returns the number of bytes used to store a sample
# 1 byte = 8 bits, so...
def samplewidth_to_bits(sw):
    return sw * 8

# The number of possible amplitude values is
# 2 to the power of the number of bits, n
# Note that we usually take a range from
# -2**(n-1), ... , 0 , ... 2**(n-1)-1
# e.g. for 16-bit samples (65536 possible values):
# -32768, ... , 0 , ... , 32767
def samplewidth_to_discrete_values(sw):
    return math.pow(2, samplewidth_to_bits(sw))

print(type(nina))

print(nina.getframerate())
print(nina.getnframes())
print(nina.getnframes() / float(nina.getframerate()))
print(nina.getsampwidth())

print(samplewidth_to_bits(nina.getsampwidth()))
print(samplewidth_to_discrete_values(nina.getsampwidth()))