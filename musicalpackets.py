import time
import thread
import sys

from mingus.midi import fluidsynth
from mingus.containers.NoteContainer import NoteContainer
from mingus.containers.Note import Note
import mingus.core.scales as scales
import mingus.core.chords as chords


import musicalDatabase
import server


class PacketListener():

    def __init__(self):
        self.clear_packet_queue()

        self._db = musicalDatabase.request_database("MusicalPackets")
        self._db_collection = self._db.open_collection("packets")

        thread.start_new_thread(self._packet_read_loop, ())

    def get_packet_queue(self):
        return self._packet_queue

    def clear_packet_queue(self):
        self._packet_queue = []

    def pop_packet_queue(self):
        packet_queue = self.get_packet_queue()
        self.clear_packet_queue()
        return packet_queue

    def _add_packet_to_queue(self, packet):
        self._packet_queue.append(packet)

    def _packet_read_loop(self):
        while True:
            line = sys.stdin.readline()
            packet = self._parse_tcpdump_line(line)

            if packet is None:
                continue
            else:
                return packet

    def _parse_tcpdump_line(self, line):
        words = line.split(" ")

        if words[1] != "IP":
            return None

        packet = {'time': time.time(),
                  'source_ip': ".".join(words[2].split(".")[:-1]),
                  'source_port': words[2].split(".")[-1],
                  'destination_ip': ".".join(words[4][:-1].split(".")[:-1]),
                  'destination_port': words[4][:-1].split(".")[-1],
                  'params': " ".join(words[4:])[:-1]
                  }

        self._add_packet_to_queue(packet)
        self._db_collection.put(packet)


class PacketAnalyser:

    _step_interval = 0.1
    _queue_length_history_length = 5
    _pps_history_length = 2

    def __init__(self, packetlistener):
        self._packetlistener = packetlistener
        self._average_pps = 0
        thread.start_new_thread(self._analyser_loop, ())

    def get_average_pps(self):
        return self._average_pps

    def _analyser_loop(self):
        queue_length_history = []
        pps_history = [0] * self._pps_history_length

        while True:
            packet_queue = self._packetlistener.pop_packet_queue()
            queue_length_history.append(len(packet_queue))

            if len(queue_length_history) == self._queue_length_history_length:
                last_pps = 0
                for queue_length in queue_length_history:
                    last_pps += queue_length

                pps_history.pop(0)
                pps_history.append(last_pps)

                self._average_pps = 0
                for pps in pps_history:
                    self._average_pps += pps
                self._average_pps /= self._pps_history_length

                queue_length_history = []

            time.sleep(self._step_interval)


class MusicalPackets:

    _step_interval = 0.5
    _current_num = 0

    def __init__(self):
        self._packetlistener = PacketListener()
        self._packetanalyser = PacketAnalyser(self._packetlistener)

        fluidsynth.init("Bandpass.sf2", 'alsa')

        self._music_loop()

    def _music_loop(self):
        current_num = 0

        while True:
            print(self._packetanalyser.get_average_pps())
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


if __name__ == "__main__":
    thread.start_new_thread(server.start, ())
    MusicalPackets()
