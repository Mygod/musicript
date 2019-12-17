from musicript import Musicript, Instrument, Track, track_worker
from musicript.temperaments import EqualTemperament12
from musicript.timbres import SineWave, WhiteNoise
from musicript.timemodifiers import Vibrato
from musicript.volumemodifiers import ExponentialDiminishingVolumeModifier


@track_worker()
def caug_arpeggiated4(duration):
    temperament(EqualTemperament12())
    c4(duration / 3); e4(duration / 3); gs4(duration / 3)


@track_worker()
def beep():
    instrument(Instrument(SineWave(), time_modifier=Vibrato())); loudness(0.5)
    temperament(EqualTemperament12())
    caug_arpeggiated4(1/2)
    c5(1/2)
    c4(); yield 1/2             # alternative way to hold time


@track_worker()
def percussion():
    instrument(Instrument(WhiteNoise(), volume_modifier=ExponentialDiminishingVolumeModifier(5))); loudness(0.2)
    while True:                 # infinite loops are okay! shorter tracks will terminate first
        note(1, 0.5)
        for i in range(4):
            note(1, 1/8)


def main():
    music = Musicript()
    music.tracks.append(Track(beep()))
    music.tracks.append(Track(percussion()))
    return music
