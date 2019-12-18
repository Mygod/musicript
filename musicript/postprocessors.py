from abc import ABC, abstractmethod
from collections import deque


class Postprocessor(ABC):
    @abstractmethod
    def process(self, sample, delta):
        return sample


class Reverb(Postprocessor):
    def __init__(self, delay, intensity):
        self.delay = delay
        self.intensity = intensity
        self.samples = deque()

    def process(self, sample, delta):
        # todo: implement a good reverb
        if len(self.samples) * delta >= self.delay:
            sample += self.samples.pop() * self.intensity
        self.samples.append(sample)
        return sample
