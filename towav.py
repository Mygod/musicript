import struct
import sys
import wave

if len(sys.argv) <= 2:
    exit("Usage: towav.py <import path> <output.wav>")
__import__(sys.argv[1])
music = sys.modules[sys.argv[1]].main()
with wave.open(sys.argv[2], 'wb') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(48000)
    while True:
        try:
            data = struct.pack('<h', int(32767 * music.update(1 / 48000)))
            wav.writeframesraw(data)
        except StopIteration:
            break
