import struct
import sys

import pyaudio

if len(sys.argv) <= 1:
    exit("Usage: tospeaker.py <import path>")
__import__(sys.argv[1])
music = sys.modules[sys.argv[1]].main()
engine = pyaudio.PyAudio()
with engine.open(format=pyaudio.paInt16, channels=1, rate=48000, output=True) as stream:
    while True:
        try:
            data = struct.pack('<h', int(32767 * music.update(1 / 48000)))
            stream.write(data)
        except StopIteration:
            break
