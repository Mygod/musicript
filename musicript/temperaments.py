import math
from abc import ABC, abstractmethod


class Temperament(ABC):
    @abstractmethod
    def setup(self, scope):
        pass


class EqualTemperament12(Temperament):
    def __init__(self, a4=440):
        self.a4 = a4

    def setup(self, scope):
        def midino(i, octave):
            return octave * 12 + [0, 2, 4, 5, 7, 9, 11][i]
        baseline = midino(5, 4)
        note = scope['note']
        for octave in range(-9, 10):
            octave_name = str(octave) if octave >= 0 else '_' + str(-octave)
            for i, letter in enumerate('cdefgab'):
                diff = midino(i, octave) - baseline
                pitch = math.pow(2, diff / 12) * self.a4
                scope[letter + octave_name] = lambda p=pitch, *args, **kwargs: note(p, *args, **kwargs)
