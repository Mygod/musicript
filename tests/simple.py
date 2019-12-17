from musicript import Musicript, Instrument, Track
from musicript.timbres import SineWave
from musicript.volume_modifiers import ExponentialDiminishingVolumeModifier


def beep():
    instrument(Instrument(SineWave(), volume_modifier=ExponentialDiminishingVolumeModifier(5))); loudness(0.5)
    note(440); yield 0.5
    note(880); yield 0.5
    note(440); yield 1


def main():
    music = Musicript()
    music.tracks.append(Track(beep()))
    return music
