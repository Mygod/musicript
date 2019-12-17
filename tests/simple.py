from musicript import Musicript, Track
from musicript.instruments import SineWave


def beep():
    instrument(SineWave()); loudness(0.5)
    note(440); yield 0.5
    note(880); yield 0.5
    note(440); yield 0.5


def main():
    music = Musicript()
    music.tracks.append(Track(beep()))
    return music
