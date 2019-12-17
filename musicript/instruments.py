import math
import random
from abc import ABC, abstractmethod


class Instrument(ABC):
    @abstractmethod
    def sample(self, time):
        pass


class SineWave(Instrument):
    def sample(self, time):
        return math.sin(2 * math.pi * time)


class SquareWave(Instrument):
    def sample(self, time):
        time - math.floor(time)
        return math.floor(time * 2) * 2 - 1


class TriangleWave(Instrument):
    def sample(self, time):
        time -= math.floor(time)
        return time * 2 - 1


class BouncySineWave(Instrument):
    def sample(self, time):
        time = math.fabs(math.sin(2 * math.pi * time))
        return time * 2 - 1


class ParabolicWave(Instrument):
    def sample(self, time):
        time -= math.floor(time) + .5
        return 1 - 8 * time * time


class SmoothParabolicWave(Instrument):
    def sample(self, time):
        time -= math.floor(time) + .5
        return 8 * time * (1 - math.fabs(time) * 2)


class WhiteNoise(Instrument):
    def sample(self, time):
        return random.uniform(-1, 1)
