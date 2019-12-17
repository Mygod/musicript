import math
import random
from abc import ABC, abstractmethod


class Timbre(ABC):
    @abstractmethod
    def sample(self, time):
        pass


class SineWave(Timbre):
    def sample(self, time):
        return math.sin(2 * math.pi * time)


class SquareWave(Timbre):
    def sample(self, time):
        time -= math.floor(time)
        return math.floor(time * 2) * 2 - 1


class TriangleWave(Timbre):
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
