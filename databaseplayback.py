import musicalDatabase
import server
import musicalpackets


class databasePacketListener():
    _packet_queue = list()

    def __init__(self, col_name):
        self._database = musicalDatabase.request_database("MusicalPackets")
        self._collection = self._database.open_collection(col_name)
        self._cursor = self._collection.find()
        self._next_packet = self._cursor.next()
        self._current_time = self._next_packet['time']

    def get_packet_queue(self):
        queue = list()
        while self._next_packet['time'] < self._current_time:
            queue.append(self._next_packet)
            self._next_packet = self._cursor.next()
        return queue

    def pop_packet_queue(self):
        self._current_time = self._current_time + musicalpackets.PacketAnalyser._step_interval
        packet_queue = self.get_packet_queue()
        return packet_queue
