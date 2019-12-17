import inspect
import types

from .timbres import Timbre
from .timemodifiers import TimeModifier, ConstantTimeModifier
from .volumemodifiers import VolumeModifier, ConstantVolumeModifier


class Musicript:
    def __init__(self):
        self.tracks = []

    def update(self, delta):
        return sum([track.update(delta) for track in self.tracks])


class Instrument:
    def __init__(self, timbre: Timbre,
                 time_modifier: TimeModifier = ConstantTimeModifier(),
                 volume_modifier: VolumeModifier = ConstantVolumeModifier()):
        self.timbre = timbre
        self.time_modifier = time_modifier
        self.volume_modifier = volume_modifier
        self.offset = 0

    def sample(self, frequency, time):
        t = self.offset + frequency * time + self.time_modifier.sample(time)
        # print(t)
        return self.timbre.sample(t) * self.volume_modifier.volume(time)

    def declick(self, frequency, time):
        self.offset += frequency * time


def bpm(i):
    return 60 / i


def setup_functions(scope):
    for key, value in inspect.stack()[1].frame.f_locals.items():
        if isinstance(value, types.FunctionType):
            scope[key] = value
