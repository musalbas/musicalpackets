import thread
import time

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


