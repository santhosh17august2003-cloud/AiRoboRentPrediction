import re
from http.server import BaseHTTPRequestHandler

from _db import get_collection
from _response import read_json, send_json


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            data = read_json(self)
            username = data.get("username")
            password = data.get("password", "")

            if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
                send_json(
                    self,
                    {"message": "Password must contain at least one special character"},
                    400,
                )
                return

            collection = get_collection()
            if collection.find_one({"username": username}):
                send_json(self, {"message": "Username already exists"}, 409)
                return

            collection.insert_one(
                {
                    "name": data.get("name"),
                    "email": data.get("email"),
                    "username": username,
                    "password": password,
                }
            )
            send_json(self, {"message": "User registered successfully"})
        except Exception as error:
            send_json(self, {"message": str(error)}, 500)
