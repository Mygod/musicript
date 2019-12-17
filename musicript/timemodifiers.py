import math
from abc import ABC, abstractmethod


class TimeModifier(ABC):
    @abstractmethod
    def sample(self, time):
        pass


class ConstantTimeModifier(TimeModifier):
    def sample(self, time):
        return 0


class Vibrato(TimeModifier):
    def __init__(self, amplitude=10, frequency=10):
        self.w = 2 * math.pi * frequency
        self.c = amplitude / self.w

    def sample(self, time):
        return (1 - math.cos(self.w * time)) * self.c
