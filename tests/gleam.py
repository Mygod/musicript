"""
Based on Sevish - Gleam: https://youtu.be/l9wINwlgxRU

A mapping of 22-TET to 12-TET:
    a     b     c     d     e     f     g     h     i     j     k     l
    A          Bb         B          C          C#         D          Eb
    l     m     n     o     p     q     r     s     t     u     v     a
    D#         E          F          F#         G          G#         A
"""
import math

from musicript import Musicript, Instrument, Track, bpm, track_worker
from musicript.articulations import MultiplicativeArticulation
from musicript.temperaments import Temperament
from musicript.timbres import TriangleWave, SquareWave


class EqualTemperament22(Temperament):
    def __init__(self, a4=440):
        self.a4 = a4

    def setup(self, gscope, lscope):
        def no(i, octave):
            return octave * 22 + i

        def make_sound(note, pitch):
            @track_worker(transform=False)  # does not work with transform yet
            def sound(*args, **kwargs):
                # print(pitch)
                for r in note(pitch, *args, **kwargs):
                    yield r
            return sound

        baseline = no(0, 4)
        note = gscope['note']
        for octave in range(-9, 10):
            octave_name = str(octave) if octave >= 0 else '_' + str(-octave)
            for i in range(22):
                lscope[chr(ord('a') + i) + octave_name] = \
                    make_sound(note, math.pow(2, (no(i, octave) - baseline) / 22) * self.a4)


@track_worker()
def melody():
    instrument(Instrument(SquareWave())); articulation(MultiplicativeArticulation())
    temperament(EqualTemperament22())
    time_scale(bpm(239))
    a4(1); h3(1/2); a4(1); a4(1/2); a4(1); e4(1)
    a4(3/2); a3(7/2)
    u2(5)
    u3(4); l3(1)
    h3(3/2); h3(3/2); h4(1); h3(1)
    g3(5/4); rest(5/4); f3(5/4); rest(5/4)
    e3(5/6); e4(5/6); p3(5/6); d3(5/6); d4(5/6); o3(5/6)
    n3(5/2); c3(1); c4(1/2); c3(1/2); c4(1/2)

    a3(4); e4(1)
    a4(3); a4(1); v3(1)
    rest(5)
    u3(3); u3(1); t3(1)
    h3(20)


@track_worker()
def bass():
    instrument(Instrument(TriangleWave())); articulation(MultiplicativeArticulation()); loudness(.03)
    temperament(EqualTemperament22())
    time_scale(bpm(239))
    a2(1); h1(1/2); a2(1); a2(1/2); a2(1); e2(1)
    a2(3/2); a1(7/2)
    rest(5)
    u1(4); l1(1)
    h1(3/2); h2(3/2); h2(1); h2(1)
    g2(5/2); f2(5/2)
    e2(5/6); e3(5/6); p2(5/6); d2(5/6); d3(5/6); o2(5/6)
    n2(5/4); n1(5/4); c2(5/2)

    a2(4); e2(1)
    a2(3); a2(1); v1(1)
    u1(3); u1(2)
    u1(3); u1(1); t1(1)
    h1(20)


def main():
    music = Musicript()
    music.tracks.append(Track(melody()))
    music.tracks.append(Track(bass()))
    return music
