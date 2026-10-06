# import os
# from pymongo import MongoClient

# def get_collection():
#     mongo_uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
#     client = MongoClient(mongo_uri)
#     db = client["robot_db"]
#     return db["users"]

# class CollectionProxy:
#     def find_one(self, *args, **kwargs):
#         return get_collection().find_one(*args, **kwargs)
        
#     def insert_one(self, *args, **kwargs):
#         return get_collection().insert_one(*args, **kwargs)

# collection = CollectionProxy()

import os
import json
import uuid
import mysql.connector


def get_connection():
    """
    Connect to Aiven MySQL
    """

    connection = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST"),
        port=int(os.environ.get("MYSQL_PORT", 3306)),
        user=os.environ.get("MYSQL_USER"),
        password=os.environ.get("MYSQL_PASSWORD"),
        database=os.environ.get("MYSQL_DATABASE"),

        # Aiven requires SSL
        ssl_disabled=False,
        ssl_verify_cert=False,
        ssl_verify_identity=False
    )

    return connection


def create_table():
    """
    Create users table if it doesn't already exist.
    """

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(100) PRIMARY KEY,
            data JSON NOT NULL
        )
    """)

    connection.commit()

    cursor.close()
    connection.close()


class CollectionProxy:
    """
    This class keeps the old MongoDB-style functions
    so the rest of your application can continue using:

        collection.find_one()
        collection.insert_one()
    """

    def find_one(self, *args, **kwargs):

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        # Example:
        # collection.find_one({"email": "abc@gmail.com"})

        query_data = args[0] if args else kwargs

        if not query_data:

            cursor.execute("""
                SELECT id, data
                FROM users
                LIMIT 1
            """)

        else:

            key = list(query_data.keys())[0]
            value = query_data[key]

            json_path = "$." + key

            cursor.execute(
                """
                SELECT id, data
                FROM users
                WHERE JSON_UNQUOTE(
                    JSON_EXTRACT(data, %s)
                ) = %s
                LIMIT 1
                """,
                (json_path, str(value))
            )

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        if result:

            data = json.loads(result["data"])

            # MongoDB-like _id
            data["_id"] = result["id"]

            return data

        return None

    def insert_one(self, *args, **kwargs):

        data = args[0] if args else kwargs

        document_id = str(uuid.uuid4())

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO users (id, data)
            VALUES (%s, %s)
            """,
            (
                document_id,
                json.dumps(data)
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        return {
            "inserted_id": document_id
        }


# Create table automatically
create_table()


# Keep the same variable name
# used by the existing application
collection = CollectionProxy()
