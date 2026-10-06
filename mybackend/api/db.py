import os
import json
import uuid
import mysql.connector


def get_connection():
    """
    Connect to Aiven MySQL
    """
    host = (os.environ.get("MYSQL_HOST") or "").strip()
    port = int(os.environ.get("MYSQL_PORT", 3306))
    user = (os.environ.get("MYSQL_USER") or "").strip()
    password = (os.environ.get("MYSQL_PASSWORD") or "").strip()
    database = (os.environ.get("MYSQL_DATABASE") or "defaultdb").strip()

    connection = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        database=database,

        # Aiven requires SSL
        ssl_disabled=False,
        ssl_verify_cert=False,
        ssl_verify_identity=False
    )

    return connection


TABLE_NAME = "robot_users"


def create_table():
    """
    Create robot_users table if it doesn't already exist.
    """
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id VARCHAR(100) PRIMARY KEY,
                data JSON NOT NULL
            )
        """)

        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print(f"[Warning] Could not initialize table {TABLE_NAME}: {e}")


class CollectionProxy:
    """
    This class keeps the MongoDB-style functions
    so the rest of your application can continue using:

        collection.find_one()
        collection.insert_one()
    """

    def find_one(self, *args, **kwargs):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        query_data = args[0] if args else kwargs

        if not query_data:
            cursor.execute(f"""
                SELECT id, data
                FROM {TABLE_NAME}
                LIMIT 1
            """)
        else:
            # Build WHERE condition for all queried fields (e.g. username AND password)
            where_clauses = []
            params = []
            for key, val in query_data.items():
                where_clauses.append("JSON_UNQUOTE(JSON_EXTRACT(data, %s)) = %s")
                params.append(f"$.{key}")
                params.append(str(val))

            sql = f"""
                SELECT id, data
                FROM {TABLE_NAME}
                WHERE {" AND ".join(where_clauses)}
                LIMIT 1
            """
            cursor.execute(sql, tuple(params))

        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
            data = json.loads(result["data"])
            data["_id"] = result["id"]
            return data

        return None

    def insert_one(self, *args, **kwargs):
        data = args[0] if args else kwargs
        document_id = str(uuid.uuid4())

        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            f"""
            INSERT INTO {TABLE_NAME} (id, data)
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

# Keep the same variable name used by the application
collection = CollectionProxy()
