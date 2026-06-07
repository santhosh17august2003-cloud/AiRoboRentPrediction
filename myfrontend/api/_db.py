import os

from pymongo import MongoClient


def get_collection():
    mongo_uri = os.environ.get("MONGODB_URI")
    if not mongo_uri:
        raise RuntimeError("MONGODB_URI environment variable is required")

    client = MongoClient(mongo_uri)
    db = client["robot_db"]
    return db["users"]
