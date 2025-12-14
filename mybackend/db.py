from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["robot_db"]          # database name
collection = db["users"]         # collection name
