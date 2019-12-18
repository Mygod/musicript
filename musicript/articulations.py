import math
from abc import ABC, abstractmethod

from musicript import track_worker


class Articulation(ABC):
    @abstractmethod
    def articulate(self, freq_set, freq, duration):
        pass


class MultiplicativeArticulation(Articulation):
    def __init__(self, k=1/16):
        self.k = k

    def articulate(self, freq_set, freq, duration):
        freq_set(freq)
        yield duration * (1 - self.k)
        freq_set(0)
        yield duration * self.k
