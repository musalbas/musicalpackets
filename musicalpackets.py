import thread
import time
import sys
from mingus.midi import fluidsynth


class PacketReader:

    step_interval = 0.1

    def __init__(self):
        self.last_step_time = time.time()
        self.packet_queue = []
        self.queue_length_history = []
        self.last_pps = 0
        self.pps_history = [0] * 10
        self.average_pps = 0

        thread.start_new_thread(self.packet_listener, ())

        fluidsynth.init("/home/mus/Downloads/Bandpass.sf2", "alsa")

        while True:
            self.queue_length_history.append(len(self.packet_queue))
            if len(self.queue_length_history) == (1 / self.step_interval):
                self.last_pps = 0
                for queue_length in self.queue_length_history:
                    self.last_pps += queue_length
                self.queue_length_history = []
                self.pps_history.pop(0)
                self.pps_history.append(self.last_pps)
                for pps in self.pps_history:
                    self.average_pps += self.last_pps
                self.average_pps /= 10

            self.packet_queue = []
            time.sleep(self.step_interval)

    def packet_listener(self):
        while True:
            line = sys.stdin.readline()
            packet = self.parse_tcpdump_line(line)
            if packet is None: continue

            fluidsynth.play_Note(self.average_pps, 0, 100)

            self.packet_queue.append(packet)

    def parse_tcpdump_line(self, line):
        words = line.split(" ")
        word_num = 0
        packet = {"params": ""}

        if words[1] != "IP":
            return None

        for word in words:
            if word_num == 0:
                packet['time'] = word
            elif word_num == 1:
                pass
            elif word_num == 3:
                pass
            elif word_num == 2:
                packet['source'] = word
            elif word_num == 4:
                packet['destination'] = word[:-1]
            else:
                packet['params'] += word + " "

            word_num += 1

        packet['params'] = packet['params'][:-2]
        return packet

if __name__ == "__main__":
    PacketReader()
