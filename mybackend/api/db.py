import os

from pymongo import MongoClient


Mongo_URI = os.environ.get("MONGODB_URI")
if not Mongo_URI:
    raise RuntimeError("MONGODB_URI environment variable is required")

client = MongoClient(Mongo_URI)
db = client["robot_db"]          
collection = db["users"]         
