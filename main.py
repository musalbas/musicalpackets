import thread
import server
from musicalpackets import MusicalPackets
from liveplayback import PacketListener
from databaseplayback import databasePacketListener
import sys

try:
    if __name__ == "__main__":
        thread.start_new_thread(server.start, ())
        if "live" in sys.argv:
            MusicalPackets(PacketListener())
        elif "playback" in sys.argv:
            MusicalPackets(databasePacketListener("packets"))
except(KeyboardInterrupt):
    print("Exiting...");

