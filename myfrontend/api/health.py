from http.server import BaseHTTPRequestHandler

from _response import send_json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        send_json(self, {"status": "ok"})
