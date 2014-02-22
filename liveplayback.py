import threading
import musicalDatabase
import sys
import time
from sniffer import Sniffer

class PacketListener():

    def __init__(self):
        self.clear_packet_queue()

        self._db = musicalDatabase.request_database("MusicalPackets")
        self._db_collection = self._db.open_collection("packets")

        networkSniffer = Sniffer()
        networkSniffer.add_callback(self)

        self._thread = threading.Thread(target=networkSniffer)
        self._thread.daemon = True
        self._thread.start()

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

    def packet_received(self, packet):
       self._add_packet_to_queue(packet)
       self._db_collection.put(packet)
