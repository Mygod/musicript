class Musicript:
    def __init__(self):
        self.tracks = []

    def update(self, time):
        return sum([track.update(time) for track in self.tracks])


class VariableScope:
    def __init__(self, scope):
        object.__setattr__(self, 'scope', scope)

    def __getattribute__(self, item):
        return object.__getattribute__(self, 'scope')[item]

    def __setattr__(self, key, value):
        object.__getattribute__(self, 'scope')[key] = value
