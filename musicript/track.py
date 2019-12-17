import types

from musicript.core import VariableScope


class Track:
    def __init__(self, generator):
        assert isinstance(generator, types.GeneratorType)
        self.generator = generator
        self.__setup()
        self.scope.instrument = None
        self.scope.frequency = 0
        self.scope.loudness = 1
        self.scope.note_time = 0
        self.next_update = 0

    def __setup(self):
        def note(f: float):
            global frequency, note_time
            frequency = f
            note_time = 0
        self.scope = VariableScope(self.generator.gi_frame.f_locals)
        self.scope.note = note

    def update(self, delta):
        assert delta >= 0   # backtracking is not allowed
        while delta >= self.next_update:
            self.scope.note_time += self.next_update
            self.next_update = next(self.generator)
            delta -= self.next_update
        try:
            if self.scope.instrument is None or self.scope.frequency < 1e-8:
                # print(self.generator.gi_frame.f_locals)
                return 0
            self.scope.note_time += delta
            return self.scope.instrument.sample(self.scope.frequency * self.scope.note_time) * self.scope.loudness
        finally:
            self.next_update -= delta
