import musicalDatabase
import time
from pymongo import DESCENDING

def _get_collection(col_name):
    database = musicalDatabase.request_database("MusicalPackets")
    return database.open_collection(col_name)

def get_total_packets(col_name):
    return _get_collection(col_name).count()

def get_packets_per_duration(col_name, per_duration=1):
    """Gets the number of packets recieved in the last X seconds."""
    cursor = _get_collection(col_name).find({'time': {'$gt': time.time() - per_duration}})
    return cursor.count()

def get_last_X_packets(col_name, packet_count=5):
    cursor = _get_collection(col_name).find().sort('time', DESCENDING).limit(5)
    packets = list()
    for data in cursor:
        del data['_id']
        packets.append(data)
    return packets


def count_field_per_duration(col_name, group_field, per_duration=1):
    result = _get_collection(col_name).aggregate([{'$match':{'time':{'$gt':time.time() - per_duration}}}, {'$group':{'_id':'$' + group_field, 'count':{'$sum':1}}}, {'$sort':{'count':-1}}])
    return result['result']
