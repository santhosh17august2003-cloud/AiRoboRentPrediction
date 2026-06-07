from http.server import BaseHTTPRequestHandler

from _db import get_collection
from _response import read_json, send_json


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            data = read_json(self)
            collection = get_collection()

            user = collection.find_one(
                {
                    "username": data.get("username"),
                    "password": data.get("password"),
                }
            )

            if user:
                send_json(self, {"message": "Login successful"})
            else:
                send_json(self, {"message": "Incorrect username or password"}, 401)
        except Exception as error:
            send_json(self, {"message": str(error)}, 500)
