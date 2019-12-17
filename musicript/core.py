import inspect
import types

from .recursiveyielder import get_worker_source
from .timbres import Timbre
from .volumemodifiers import VolumeModifier, ConstantVolumeModifier


class Musicript:
    def __init__(self):
        self.tracks = []

    def update(self, delta):
        return sum([track.update(delta) for track in self.tracks])


class Instrument:
    def __init__(self, timbre: Timbre, volume_modifier: VolumeModifier = ConstantVolumeModifier()):
        self.timbre = timbre
        self.volume_modifier = volume_modifier
        self.offset = 0

    def sample(self, frequency, time):
        # print(self.offset + frequency * time)
        return self.timbre.sample(self.offset + frequency * time) * self.volume_modifier.volume(time)

    def declick(self, frequency, time):
        self.offset += frequency * time


def setup_functions(scope):
    for key, value in inspect.stack()[1].frame.f_locals.items():
        if isinstance(value, types.FunctionType):
            scope[key] = value
