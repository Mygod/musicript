from musicript import Musicript, Instrument, Track, bpm, track_worker
from musicript.temperaments import Midi
from musicript.timbres import SquareWave


@track_worker()
def beep():
    instrument(Instrument(SquareWave())); loudness(0.1)
    temperament(Midi())
    time_scale(bpm(108))
    for i in range(128):
        midi(i, 1/4)


def main():
    music = Musicript()
    music.tracks.append(Track(beep()))
    return music
