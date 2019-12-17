import math
from abc import ABC, abstractmethod


class VolumeModifier(ABC):
    @abstractmethod
    def volume(self, time):
        pass


class ConstantVolumeModifier(VolumeModifier):
    def volume(self, time):
        return 1


class ExponentialDiminishingVolumeModifier(VolumeModifier):
    def __init__(self, rate=5):
        self.rate = rate

    def volume(self, time):
        return math.exp(-self.rate * time)
