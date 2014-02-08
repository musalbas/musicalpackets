from pymongo import MongoClient

_database_objects = dict()

class _database_object:
    #_database - The database object
    def open_collection(self, collection_name):
        collection = _collection_object()
        collection._collection = self._database[collection_name]
        return collection

class _collection_object:
    def find(self, query={}):
        return self._collection.find(query)

    def aggregate(self, query={}):
        return self._collection.aggregate(query)
    
    def put(self, packet_dict):
        self._collection.insert(packet_dict)

    def count(self):
        return self._collection.count()

        
    
def _create_database_object(db_name):
    client = MongoClient()
    db_obj = _database_object()
    db_obj._database = client[db_name] 
    return db_obj

def request_database(db_name):
    if not db_name in _database_objects:
        _database_objects[db_name] = _create_database_object(db_name)
    return _database_objects[db_name]

