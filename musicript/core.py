import inspect
import types

from .timbres import Timbre
from .volume_modifiers import VolumeModifier, ConstantVolumeModifier


class Musicript:
    def __init__(self):
        self.tracks = []

    def update(self, delta):
        return sum([track.update(delta) for track in self.tracks])


class Instrument:
    def __init__(self, timbre: Timbre, volume_modifier: VolumeModifier = ConstantVolumeModifier()):
        self.timbre = timbre
        self.volume_modifier = volume_modifier

    def sample(self, frequency, time):
        return self.timbre.sample(frequency * time) * self.volume_modifier.volume(time)


def setup_functions(scope):
    for key, value in inspect.stack()[1].frame.f_locals.items():
        if isinstance(value, types.FunctionType):
            scope[key] = value
