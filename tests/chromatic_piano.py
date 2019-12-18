from musicript import Musicript, Instrument, Track, bpm, track_worker
from musicript.temperaments import Midi
from musicript.timbres import SumTimbre, SineWave
from musicript.volumemodifiers import ExponentialDiminishingVolumeModifier


class PianoTimbre(SumTimbre):
    def __init__(self):
        super().__init__(
            # data from: https://slideplayer.com/slide/7071199/
            SineWave(1) * .29,
            SineWave(2) * .395,
            SineWave(3) * .03,
            SineWave(4) * .02,
            SineWave(5) * .045,
            SineWave(6) * .01,
            SineWave(7) * .075,
            SineWave(8) * .015,
        )


@track_worker()
def beep():
    instrument(Instrument(PianoTimbre(), volume_modifier=ExponentialDiminishingVolumeModifier(5))); loudness(0.1)
    temperament(Midi())
    time_scale(bpm(108))
    for i in range(21, 109):
        midi(i, 1/4)


def main():
    music = Musicript()
    music.tracks.append(Track(beep()))
    return music
