import math
from abc import ABC, abstractmethod

from . import track_worker


def make_sound(note, pitch):
    @track_worker(transform=False)  # does not work with transform yet
    def sound(*args, **kwargs):
        # print(pitch)
        for r in note(pitch, *args, **kwargs):
            yield r
    return sound


class Temperament(ABC):
    @abstractmethod
    def setup(self, gscope, lscope):
        pass


class Midi(Temperament):
    def __init__(self, a4=440):
        self.a4 = a4

    def setup(self, gscope, lscope):
        @track_worker(transform=False)
        def midi(midino, *args, **kwargs):
            pitch = math.pow(2, (midino - 69) / 12) * self.a4
            # print(pitch)
            for r in note(pitch, *args, **kwargs):
                yield r
        note = gscope['note']
        lscope['midi'] = midi


class EqualTemperament12(Temperament):
    def __init__(self, a4=440):
        self.a4 = a4

    def setup(self, gscope, lscope):
        def midino(i, octave):
            return octave * 12 + [0, 2, 4, 5, 7, 9, 11][i]
        baseline = midino(5, 4)
        note = gscope['note']
        for octave in range(-9, 10):
            octave_name = str(octave) if octave >= 0 else '_' + str(-octave)
            for i, letter in enumerate('cdefgab'):
                diff = midino(i, octave) - baseline
                for j, suffix in enumerate(['bb', 'b', '', 's', 'x']):
                    lscope[letter + suffix + octave_name] = make_sound(note, math.pow(2, (diff + j - 2) / 12) * self.a4)
