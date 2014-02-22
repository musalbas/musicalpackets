import time
from packetanalysers import PacketAnalyser

from mingus.midi import fluidsynth
from mingus.containers.NoteContainer import NoteContainer
from mingus.containers.Note import Note
import mingus.core.scales as scales
import mingus.core.chords as chords




class MusicalPackets:

    _step_interval = 0.5
    _current_num = 0

    def __init__(self, packetlistener):
        self._packetlistener = packetlistener
        self._packetanalyser = PacketAnalyser(self._packetlistener)

        fluidsynth.init("Bandpass.sf2", 'alsa')

        self._music_loop()

    def _music_loop(self):
        while True:
            self._current_num = self._packetanalyser.get_average_pps() % 85
            self.play_note(discord=0)
            time.sleep(self._step_interval)
            self.stop_note()

    def play_note(self, discord=0):
        if discord:
            self._current_note = self.generate_discord_container(self._current_num)
        elif self._current_num == 0:
            self._current_note = self.generate_base_container("C")
        else:
            self._current_note = self.generate_triad_container(self._current_num, "C")
        fluidsynth.play_NoteContainer(self._current_note, 0, 100)

    def stop_note(self):
        fluidsynth.stop_NoteContainer(self._current_note, 0)

    def generate_triad_container(self, number, key):
        scale = scales.diatonic(key)
        pos = number % len(scale)
        triad = chords.triad(scale[pos], key)
        return NoteContainer(triad)

    def generate_discord_container(self, number):
        return NoteContainer(Note(number))

    def generate_base_container(self, key):
        return NoteContainer(Note(scales.diatonic(key)[0], 2))


