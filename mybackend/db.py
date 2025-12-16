from pymongo import MongoClient

Mongo_URI = "mongodb+srv://santhosh17august2003_db_user:eTfNojfB3duRjyoW@cluster0.ldhuyot.mongodb.net/?appName=Cluster0"
client = MongoClient(Mongo_URI)
db = client["robot_db"]          
collection = db["users"]         
