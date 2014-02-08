import musicalDatabase
import time

def _get_collection(col_name):
    database = musicalDatabase.request_database("MusicalPackets")
    return database.open_collection(col_name)

def get_total_packets(col_name):
    return _get_collection(col_name).count()

def get_packets_per_duration(col_name, per_duration=1):
    """Gets the number of packets recieved in the last X seconds."""
    cursor = _get_collection(col_name).find({'time': {'$gt': time.time() - per_duration}})
    return cursor.count()

def count_field_per_duration(col_name, group_field, per_duration=1):
    result = _get_collection(col_name).aggregate([{'$group':{'_id':'$' + group_field, 'count':{'$sum':1}}}, {'$sort':{'count':-1}}])
    return result['result']
