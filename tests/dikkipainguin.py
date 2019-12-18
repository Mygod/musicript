# this is a transcription of: https://www.youtube.com/watch?v=hR2HnsUIvW8

from musicript import Musicript, Instrument, Track, bpm, track_worker
from musicript.articulations import MultiplicativeArticulation
from musicript.temperaments import EqualTemperament12
from musicript.timbres import SawtoothWave, SquareWave, WhiteNoise


@track_worker()
def bop(duration):
    note(1, 1/8)
    rest(duration - 1/8)


@track_worker()
def perc(rep):
    instrument(Instrument(WhiteNoise()))
    for r in range(rep):
        time_scale(bpm(145))
        for i in range(8): bop(1/2); bop(1/4); bop(1/4)

        time_scale(bpm(141.2))
        bop(1); bop(1/2); bop(1/2)
        bop(1); bop(1/2); bop(1/4); bop(1/4)
        for i in range(6): bop(1/2)
        # 1 + 4 (A) 12 + 1
        for i in range(1 + 4 + 12 + 1): bop(1/2); bop(1/4); bop(1/4)
        for i in range(12): bop(1/4)
        # B
        for j in range(8): bop(1/2)
        for j in range(3): bop(1/2); bop(1/4); bop(1/4)
        for j in range(4): bop(1/4)
        # 16 (C) 24 + 1
        for j in range(16 + 24 + 1): bop(1/2)
        for j in range(14): bop(1/4)
        # D
        for i in range(8): bop(1/2); bop(1/4); bop(1/4)


@track_worker()
def bass_rif(a):
    for i in range(3): a(1/2)
    for i in range(2): a(1/4)


@track_worker()
def bass(rep, a4):
    instrument(Instrument(SquareWave())); articulation(MultiplicativeArticulation())
    temperament(EqualTemperament12(a4))
    for r in range(rep):
        time_scale(bpm(145))
        for i in range(16): fs3(1/2)

        time_scale(bpm(141.2))
        gs2(1/2); rest(1/2); ds3(1); gs3(1); as3(1)
        e2(1/2); e2(1/2); e3(1); b3(1); cs4(1)
        fs2(1/2); fs2(1/2); cs4(1); b3(1); as3(1)

        # A
        bass_rif(gs3)
        for i in range(4): gs3(1/2)
        for i in range(2): bass_rif(e3)
        for i in range(2): bass_rif(fs2)

        for i in range(2): fs2(1/2); fs2(1/4); fs2(1/4)
        ds4(1); fs4(1)
        for i in range(2):
            # 1st time B; 2nd time C
            for j in range(8): e2(1/2)
            gs2(1/2); e4(1); ds4(1/2)
            e4(1); b3(1/2); as3(1/2)
            bass_rif(fs2)
            bass_rif(gs2)
            bass_rif(as2)
            ds4(1); fs4(1)
        # D
        for i in range(2):
            for j in range(4): gs2(1/2)
            bass_rif(gs2)


@track_worker()
def countermelody_rifb(a, b, c, d, e):
    d(1/4); e(1/4); c(1/4); b(1/4)
    d(1/4); c(1/4); b(1/4); a(1/4)


@track_worker()
def countermelody(rep, a4):
    instrument(Instrument(SquareWave())); articulation(MultiplicativeArticulation())
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
        for i in range(2):
            # 1st time B; 2nd time C
            gs4(2); as4(2); b4(4)
            countermelody_rifb(fs3, as3, cs4, ds4, fs4)
            countermelody_rifb(gs3, b3, ds4, e4, gs4)
            countermelody_rifb(as3, cs4, e4, fs4, as4)
            countermelody_rifb(b3, ds4, fs4, gs4, b4)
        gs4(2); rest(1/2); fs4(1); ds4(1/2)
        ds4(4)


@track_worker()
def melody_rifb1(a, b, c):
    for i in range(2): a(1/4); c(1/4); b(1/4); c(1/4)


@track_worker()
def melody_rifb2(a, b, c):
    c(1/4); b(1/4); a(1/4); b(1/4)
    b(1/4); b(1/4); a(1/4); b(1/4)


@track_worker()
def melody(rep, a4):
    instrument(Instrument(SawtoothWave())); articulation(MultiplicativeArticulation())
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
        for i in range(2):
            # 1st time B; 2nd time C
            melody_rifb1(gs4, as4, b4)
            melody_rifb1(as4, b4, cs5)
            if i == 0:
                melody_rifb1(b4, cs5, ds5)
                melody_rifb1(cs5, ds5, e5)
            else:
                b4(1/4); ds5(1/4); ds5(1/4); e5(1/4)
                ds5(1/4); e5(1/4); cs5(1/4); ds5(1/4)
                ds5(1/4); cs5(1/4); as4(1/4); b4(1/4)
                gs4(1/4); as4(1/4); fs4(1/4); gs4(1/4)
            melody_rifb2(e4, fs4, as4)
            melody_rifb2(fs4, gs4, b4)
            melody_rifb2(gs4, as4, cs5)
            melody_rifb2(as4, b4, ds5)
        # D
        for i in [0, 2, 3, 5, 7, 8, 10, 11]:
            tp.shift = i    # gs as b cs ds e fs fx
            gs3(1/2); gs4(1/2)
        tp.shift = 0


def main():
    rep = 2
    a4 = 432
    music = Musicript()
    music.tracks.append(Track(melody(rep, a4)))
    music.tracks.append(Track(countermelody(rep, a4)))
    music.tracks.append(Track(bass(rep, a4)))
    music.tracks.append(Track(perc(rep)))
    return music
