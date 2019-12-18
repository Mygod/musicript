import math
import random
from abc import ABC, abstractmethod


class Timbre(ABC):
    @abstractmethod
    def sample(self, time):
        pass

    def __mul__(self, other):
        return ScaledTimbre(self, other)


class ScaledTimbre(Timbre):
    def __init__(self, timbre, scale):
        self.timbre = timbre
        self.scale = scale

    def sample(self, time):
        return self.timbre.sample(time) * self.scale


class SumTimbre(Timbre):
    def __init__(self, *args):
        self.timbres = args

    def sample(self, time):
        return sum([timbre.sample(time) for timbre in self.timbres])


class SineWave(Timbre):
    def __init__(self, freq=1):
        self.k = 2 * math.pi * freq

    def sample(self, time):
        return math.sin(self.k * time)


class SquareWave(Timbre):
    def sample(self, time):
        time -= math.floor(time)
        return math.floor(time * 2) * 2 - 1


class TriangleWave(Timbre):
    def sample(self, time):
        time -= math.floor(time)
        return math.fabs(time * 2 - 1) * 2 - 1


class SawtoothWave(Timbre):
    def sample(self, time):
        time -= math.floor(time)
        return time * 2 - 1


class BouncySineWave(Timbre):
    def sample(self, time):
        time = math.fabs(math.sin(2 * math.pi * time))
        return time * 2 - 1


class ParabolicWave(Timbre):
    def sample(self, time):
        time -= math.floor(time) + .5
        return 1 - 8 * time * time


class SmoothParabolicWave(Timbre):
    def sample(self, time):
        time -= math.floor(time) + .5
        return 8 * time * (1 - math.fabs(time) * 2)


class WhiteNoise(Timbre):
    def sample(self, time):
        return random.uniform(-1, 1)
