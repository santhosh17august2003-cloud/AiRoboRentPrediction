import json


def read_json(handler):
    length = int(handler.headers.get("content-length", 0))
    raw_body = handler.rfile.read(length).decode("utf-8")
    return json.loads(raw_body or "{}")


def send_json(handler, payload, status=200):
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)
