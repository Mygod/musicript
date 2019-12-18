# this is a transcription of: https://www.youtube.com/watch?v=7FeH_yOLosU

from musicript import Musicript, Instrument, Track, bpm, track_worker
from musicript.temperaments import EqualTemperament12
from musicript.timbres import SawtoothWave, SquareWave
from musicript.volumemodifiers import ExponentialDiminishingVolumeModifier


@track_worker()
def bass(rep, a4):
    instrument(Instrument(SquareWave())); articulation(1/16)
    temperament(EqualTemperament12(a4))
    for r in range(rep):
        time_scale(bpm(145))
        for i in range(16): fs3(1/2)

        time_scale(bpm(141.2))
        gs2(1/2); rest(1/2); ds3(1); gs3(1); as3(1)
        e2(1/2); e2(1/2); e3(1); b3(1); cs4(1)
        fs2(1/2); fs2(1/2); cs4(1); b3(1); as3(1)

        # A
        for i in range(3): gs3(1/2)
        gs3(1/4); gs3(1/4)
        for i in range(4): gs3(1/2)
        for j in range(2):
            for i in range(3): e3(1/2)
            e3(1/4); e3(1/4)
        for j in range(2):
            for i in range(3): fs2(1/2)
            fs2(1/4); fs2(1/4)

        fs2(1/2); fs2(1/4); fs2(1/4)
        fs2(1/2); fs2(1/4); fs2(1/4)
        ds4(1); fs4(1)


@track_worker()
def countermelody(rep, a4):
    instrument(Instrument(SquareWave())); articulation(1/16)
    tp = EqualTemperament12(a4)
    temperament(tp)
    for r in range(rep):
        time_scale(bpm(145))
        for i in range(2):
            tp.shift = i * 12   # up an octave second time
            gs2(1/4); as2(1/4); ds3(1/2)
            ds3(1/4); fs3(1/4); gs3(1/2)
            gs3(1/4); as3(1/4); b3(1/2)
            b3(1/4); cs4(1/4); ds4(1/2)
        tp.shift = 0
        time_scale(bpm(141.2))
        for i in range(2):
            # 2nd time: A
            gs4(1/2); ds4(1/2); gs4(1/2); as4(1/2)
            rest(1/2); ds4(1/2); as4(1/2); b4(1/2)
            rest(1/2); e4(1/2); b4(1/2); cs5(1/2)
            b4(1/2); e4(1/2); as4(1/2); gs4(1/2)
            gs4(1/2); fs4(1/2); b3(1/2); rest(1/2)
            as4(1/4); fs4(1/4); cs4(1/4); as3(1/4)
            fs4(1/4); cs4(1/4); as3(1/4); fs3(1/4)
        gs4(1/2); fs4(1/2); b3(1/2); rest(1/2)
        as4(1/4); fs4(1/4); cs4(1/4); as3(1/4)
        fs4(1/4); cs4(1/4); as3(1/4); fs3(1/4)


@track_worker()
def melody(rep, a4):
    instrument(Instrument(SawtoothWave())); articulation(1/16)
    tp = EqualTemperament12(a4)
    temperament(tp)
    for r in range(rep):
        time_scale(bpm(145))
        for i in range(2):
            tp.shift = i * 12   # up an octave second time
            b2(1/4); cs3(1/4); fs3(1/2)
            fs3(1/4); as3(1/4); b3(1/2)
            b3(1/4); cs4(1/4); ds4(1/2)
            ds4(1/4); e4(1/4); fs4(1/2)
        tp.shift = 0
        time_scale(bpm(141.2))
        for i in range(2):
            # 2nd time: A
            gs4(1/2); as4(1/2); b4(1/2); as4(1/2)
            rest(1/2); as4(1/2); gs4(1/2); e5(1)
            ds5(1/2); e5(1)
            rest(1/2); as4(1/2); b4(1/2); ds5(1/2)
            fs5(1/4); cs5(1/4); as4(1/4); fs4(1/4)
            cs5(1/4); as4(1/4); fs4(1/4); cs4(1/4)
            as4(1/4)
            for j in range(4): fs4(1/4)
            rest(3/4)
        fs5(1/4); cs5(1/4); as4(1/4); fs4(1/4)
        cs5(1/4); as4(1/4); fs4(1/4); cs4(1/4)
        as4(1/4); fs4(1/4); cs4(1/4); as3(1/4)
        fs4(1/4); cs4(1/4); as3(1/4); cs5(1/4)


def main():
    rep = 1
    a4 = 432
    music = Musicript()
    music.tracks.append(Track(melody(rep, a4)))
    music.tracks.append(Track(countermelody(rep, a4)))
    music.tracks.append(Track(bass(rep, a4)))
    return music
