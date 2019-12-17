import types

from .core import Instrument, isolate_globals, setup_functions
from .temperaments import Temperament


class Track:
    def __init__(self, generator):
        generator = isolate_globals(generator)()
        assert isinstance(generator, types.GeneratorType)
        self.generator = generator
        self.next_update = 0
        self.__setup()
        self.instrument = None
        self.frequency = 0
        self.loudness = .01
        self.note_time = 0

    def __setup(self):
        def frequency(f: float):
            self.frequency = f

        def instrument(i: Instrument):
            self.instrument = i

        def loudness(l: float):
            self.loudness = l

        def note(f: float):
            self.frequency = f
            self.note_time = 0

        def temperament(t: Temperament):
            t.setup(self.generator.gi_frame.f_globals)

        setup_functions(self.generator.gi_frame.f_globals)

    def update(self, delta):
        assert delta >= 0   # backtracking is not allowed
        while delta >= self.next_update:
            delta -= self.next_update
            self.note_time += self.next_update
            self.next_update = next(self.generator)
        self.next_update -= delta
        if self.instrument is None or self.frequency < 1e-8:
            # print(self.generator.gi_frame.f_globals)
            return 0
        self.note_time += delta
        return self.instrument.sample(self.frequency, self.note_time) * self.loudness
