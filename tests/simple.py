from musicript import Musicript, Instrument, Track
from musicript.timbres import SineWave, WhiteNoise
from musicript.volume_modifiers import ExponentialDiminishingVolumeModifier


def beep():
    instrument(Instrument(SineWave())); loudness(0.5)
    note(440); yield 0.5
    note(880); yield 0.5
    note(440); yield 0.5


def percussion():
    instrument(Instrument(WhiteNoise(), volume_modifier=ExponentialDiminishingVolumeModifier(5))); loudness(0.2)
    note(1); yield 0.5
    note(1); yield 0.25
    note(1); yield 0.25
    note(1); yield 0.5


def main():
    music = Musicript()
    music.tracks.append(Track(beep))
    music.tracks.append(Track(percussion))
    return music
