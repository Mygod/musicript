from musicript import Musicript, Instrument, Track, bpm, track_worker
from musicript.temperaments import EqualTemperament12
from musicript.timbres import SawtoothWave, SquareWave


@track_worker()
def bass_fsm():
    temperament(EqualTemperament12())
    fs2(1/2); a2(1/2); cs3(1/2); fs3(1/2)
    a3(1/2); fs3(1/2); cs3(1/2); a2(1/2)


@track_worker()
def bass_d():
    temperament(EqualTemperament12())
    d2(1/2); fs2(1/2); a2(1/2); d3(1/2)
    fs3(1/2); d3(1/2); a2(1/2); fs2(1/2)


@track_worker()
def bass_cs():
    temperament(EqualTemperament12())
    cs2(1/2); es2(1/2); gs2(1/2); cs3(1/2)
    es3(1/2); cs3(1/2); gs2(1/2); es2(1/2)


@track_worker()
def bass():
    instrument(Instrument(SawtoothWave())); loudness(.02)
    time_scale(bpm(240))
    bass_fsm()
    bass_fsm()
    bass_d()
    bass_cs()
    bass_fsm()


@track_worker()
def countermelody():
    instrument(Instrument(SquareWave()))
    time_scale(bpm(240))
    temperament(EqualTemperament12())
    yield 8
    d4(4)
    es4(4)
    fs4(4)


@track_worker()
def melody():
    instrument(Instrument(SawtoothWave())); loudness(.02)
    time_scale(bpm(240))
    temperament(EqualTemperament12())
    articulation(1/16)
    yield 2; fs4(1); cs5(1)
    a5(1); fs5(1); cs5(1); a4(1)
    fs5(1); fs5(1); fs5(1); fs5(1)
    es5(1); es5(1); es5(1); es5(1)
    fs4(1); fs4(1); fs4(1); fs4(1)


def main():
    music = Musicript()
    music.tracks.append(Track(melody()))
    music.tracks.append(Track(countermelody()))
    music.tracks.append(Track(bass()))
    return music
