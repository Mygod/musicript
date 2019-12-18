import inspect
import types

from . import Instrument, track_worker
from .core import setup_functions
from .temperaments import Temperament


class Track:
    def __init__(self, generator):
        assert isinstance(generator, types.GeneratorType)
        self.generator = generator
        self.next_update = 0
        self.__setup()
        self.instrument = None
        self.frequency = 0
        self.loudness = .01
        self.note_time = 0
        self.declick = True
        self.time_scale = 1
        self.articulation = 0

    def __setup(self):
        def articulation(a: float):
            self.articulation = a

        def declick(d: bool):
            self.declick = d

        def frequency(f: float):
            self.frequency = f

        def instrument(i: Instrument):
            self.instrument = i

        def loudness(l: float):
            self.loudness = l

        @track_worker(transform=False)
        def note(f: float, duration=None):
            self.frequency = f
            self.note_time = 0
            if duration is not None:
                if self.articulation > 0:
                    yield duration * (1 - self.articulation)
                    self.frequency = 0
                    yield duration * self.articulation
                else:
                    yield duration

        def temperament(t: Temperament):
            # print(inspect.stack()[2].frame)
            t.setup(self.generator.gi_frame.f_globals, inspect.stack()[2].frame.f_globals)

        def time_scale(t: float):
            self.time_scale = t

        setup_functions(self.generator.gi_frame.f_globals)

    def update(self, delta):
        assert delta >= 0   # backtracking is not allowed
        if delta >= self.next_update:
            if self.declick and self.instrument is not None:
                self.instrument.declick(self.frequency, self.note_time)
            while delta >= self.next_update:
                delta -= self.next_update
                self.note_time += self.next_update
                self.next_update = next(self.generator) * self.time_scale
        self.next_update -= delta
        if self.instrument is None or self.frequency < 1e-8:
            # print(self.generator.gi_frame.f_globals)
            return 0
        self.note_time += delta
        return self.instrument.sample(self.frequency, self.note_time) * self.loudness
