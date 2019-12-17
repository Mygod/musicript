import struct
import wave

from musicript import Musicript, Track
from musicript.instruments import SineWave


# noinspection PyUnusedLocal
def beep():
    instrument = SineWave(); loudness = 0.5
    frequency = 440
    yield 2


def sine():
    music = Musicript()
    music.tracks.append(Track(beep()))
    return music


music = sine()
with wave.open('sine.wav', 'wb') as wav:
    wav.setnchannels(1)
    wav.setsampwidth(2)
    wav.setframerate(44100)
    while True:
        try:
            data = struct.pack('<h', int(32767 * music.update(1 / 44100)))
            wav.writeframesraw(data)
        except StopIteration:
            break
