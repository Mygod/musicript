import inspect
import types


class Musicript:
    def __init__(self):
        self.tracks = []

    def update(self, time):
        return sum([track.update(time) for track in self.tracks])


def setup_functions(scope):
    for key, value in inspect.stack()[1].frame.f_locals.items():
        if isinstance(value, types.FunctionType):
            scope[key] = value
