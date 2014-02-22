import thread
import musicalDatabase
import sys

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
            if not line:
                continue
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


