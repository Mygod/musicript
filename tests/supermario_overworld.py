# this needs no introduction

from musicript import Musicript, Instrument, Track, bpm, track_worker
from musicript.articulations import Articulation
from musicript.temperaments import EqualTemperament12
from musicript.timbres import SawtoothWave, SquareWave, WhiteNoise


class MarioOverworldArticulation(Articulation):
    def articulate(self, freq_set, freq, duration):
        freq_set(freq)
        yield 1/2 - 1/16
        freq_set(0)
        yield duration - (1/2 - 1/16)


@track_worker()
def perc(rep):
    pass    # todo?


@track_worker()
def bass_intro():
    temperament(EqualTemperament12())
    d3(1/2); d3(1); d3(1); d3(1/2); d3(1)
    g4(2); g3(2)


@track_worker()
def bass_rifa():
    temperament(EqualTemperament12())
    c3(3/2); g3(3/2); c4(1)
    f3(3/2); c4(1/2); c4(1); f3(1)


@track_worker()
def bass_c():
    temperament(EqualTemperament12())
    for i in range(2):
        g3(3/2); e3(3/2); c3(3/2)
        f3(1); g3(1/2)
        rest(1/2); gb3(1/2); f3(1)
        e3(2/3); c4(2/3); e4(2/3)
        f4(1); d4(1/2); e4(1/2)
        rest(1/2); c4(1); a3(1/2)
        b3(1/2); g3(3/2)


@track_worker()
def bass(rep):
    instrument(Instrument(SquareWave())); articulation(MarioOverworldArticulation())
    time_scale(bpm(200))
    temperament(EqualTemperament12())
    bass_intro()
    for r in range(rep):
        bass_c()
        for i in range(2):
            bass_rifa()
            c3(3/2); e3(3/2); g3(1/2); c4(1/2)
            rest(1/2); f5(1); f5(1/2)
            f5(1); g3(1)
            bass_rifa()
            c3(1); ab3(3/2)
            bb3(3/2)
            c4(3/2); g3(1/2)
            g3(1); c3(1)
        for i in range(2):
            for j in range(3):
                ab2(3/2); eb3(3/2); ab3(1)
                g3(3/2); c3(3/2); g2(1)
            bass_intro()
        bass_c()


@track_worker()
def countermelody_intro():
    temperament(EqualTemperament12())
    fs4(1/2); fs4(1); fs4(1); fs4(1/2); fs4(1)
    b4(2); g4(2)


@track_worker()
def countermelody_rifa1():
    temperament(EqualTemperament12())
    rest(1); e5(1/2); eb5(1/2)
    d5(1/2); b4(1); c5(1/2)


@track_worker()
def countermelody_rifa2():
    countermelody_rifa1()
    temperament(EqualTemperament12())
    rest(1/2); e4(1/2); f4(1/2); g4(1/2)
    rest(1/2); c4(1/2); e4(1/2); f4(1/2)


@track_worker()
def countermelody_rifb1():
    temperament(EqualTemperament12())
    ab4(1/2); ab4(1); ab4(1); ab4(1/2); bb4(1/2)


@track_worker()
def countermelody_rifb2():
    countermelody_rifb1(); rest(1/2)
    temperament(EqualTemperament12())
    g4(1/2); e4(1); e4(1/2); c4(2)


@track_worker()
def countermelody_c():
    temperament(EqualTemperament12())
    for i in range(2):
        e4(3/2); c4(3/2); g3(3/2)
        c4(1); d4(1/2)
        rest(1/2); db4(1/2); c4(1)
        c4(2/3); g4(2/3); b4(2/3)
        c5(1); a4(1/2); b4(1/2)
        rest(1/2); a4(1); e4(1/2)
        f4(1/2); d4(3/2)


@track_worker()
def countermelody(rep):
    instrument(Instrument(SquareWave())); articulation(MarioOverworldArticulation())
    time_scale(bpm(200))
    temperament(EqualTemperament12())
    countermelody_intro()
    for r in range(rep):
        countermelody_c()
        for i in range(2):
            countermelody_rifa2()
            countermelody_rifa1()
            rest(1/2); g5(1); g5(1/2)
            g5(2)
            countermelody_rifa2()
            rest(1); ab4(3/2); f4(3/2)
            e4(4)
        for i in range(2):
            countermelody_rifb2()
            countermelody_rifb1(); g4(1/2)
            rest(4)
            countermelody_rifb2()
            countermelody_intro()
        countermelody_c()


@track_worker()
def melody_intro():
    temperament(EqualTemperament12())
    e5(1/2); e5(1); e5(1); c5(1/2); e5(1)
    g5(2); g4(2)


@track_worker()
def melody_rifa1():
    temperament(EqualTemperament12())
    rest(1); g5(1/2); gb5(1/2)
    f5(1/2); ds5(1); e5(1/2)


@track_worker()
def melody_rifa2():
    melody_rifa1()
    temperament(EqualTemperament12())
    rest(1/2); gs4(1/2); a4(1/2); c5(1/2)
    rest(1/2); a4(1/2); c5(1/2); d5(1/2)


@track_worker()
def melody_rifb1():
    temperament(EqualTemperament12())
    c5(1/2); c5(1); c5(1); c5(1/2); d5(1/2)


@track_worker()
def melody_rifb2():
    melody_rifb1(); rest(1/2)
    temperament(EqualTemperament12())
    e5(1/2); c5(1); a4(1/2); g4(2)


@track_worker()
def melody_c():
    temperament(EqualTemperament12())
    for i in range(2):
        c5(3/2); g4(3/2); e4(3/2)
        a4(1); b4(1/2)
        rest(1/2); bb4(1/2); a4(1)
        g4(2/3); e5(2/3); g5(2/3)
        a5(1); f5(1/2); g5(1/2)
        rest(1/2); e5(1); c5(1/2)
        d5(1/2); b4(3/2)


@track_worker()
def melody(rep):
    instrument(Instrument(SawtoothWave())); articulation(MarioOverworldArticulation())
    time_scale(bpm(200))
    temperament(EqualTemperament12())
    melody_intro()
    for r in range(rep):
        melody_c()
        for i in range(2):
            melody_rifa2()
            melody_rifa1()
            rest(1/2); c6(1); c6(1/2)
            c6(2)
            melody_rifa2()
            rest(1); eb5(3/2); d5(3/2)
            c5(4)
        for i in range(2):
            melody_rifb2()
            melody_rifb1(); e5(1/2)
            rest(4)
            melody_rifb2()
            melody_intro()
        melody_c()


def main():
    rep = 2
    music = Musicript()
    music.tracks.append(Track(melody(rep)))
    music.tracks.append(Track(countermelody(rep)))
    music.tracks.append(Track(bass(rep)))
    # music.tracks.append(Track(perc(rep)))
    return music
