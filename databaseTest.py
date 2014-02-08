import musicalDatabase
import musicalStatistics as stats
from getdata import getdata
import time

database = musicalDatabase.request_database("MusicalPackets")
database._database.drop_collection("MyFirstMusic")
collection = database.open_collection("MyFirstMusic")


data = getdata()
global counter
counter = 0
for packet in data:
    counter = counter + 1
    packet['time'] = time.time() + counter
    collection.put(packet)

result = stats.count_field_per_duration("MyFirstMusic", 'source', 5)

