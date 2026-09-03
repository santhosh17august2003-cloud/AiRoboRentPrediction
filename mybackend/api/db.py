import os
from pymongo import MongoClient

def get_collection():
    mongo_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client["robot_db"]
    return db["users"]

class CollectionProxy:
    def find_one(self, *args, **kwargs):
        return get_collection().find_one(*args, **kwargs)
        
    def insert_one(self, *args, **kwargs):
        return get_collection().insert_one(*args, **kwargs)

collection = CollectionProxy()
