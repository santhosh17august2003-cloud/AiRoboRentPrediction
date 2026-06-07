import pickle
from http.server import BaseHTTPRequestHandler
from pathlib import Path

import numpy as np

from _response import read_json, send_json


MODEL_PATH = Path(__file__).with_name("model.pkl")
model = pickle.load(open(MODEL_PATH, "rb"))


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            data = read_json(self)
            features = np.array(
                [
                    [
                        int(data["num_robots"]),
                        int(data["hour"]),
                        int(data["num_days"]),
                    ]
                ]
            )
            prediction = model.predict(features)
            send_json(self, {"prediction": round(float(prediction[0]), 2)})
        except Exception as error:
            send_json(self, {"message": str(error)}, 500)
