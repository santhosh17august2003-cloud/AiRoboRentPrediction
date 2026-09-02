import os
import re
import pickle
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from api.db import collection

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

MODEL_PATH = Path(__file__).parent.parent / "model.pkl"
model2 = pickle.load(open(MODEL_PATH, "rb"))

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "message": "Backend server is active"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    password = data["password"]
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return jsonify({
            "message": "Password must contain at least one special character"
        }), 400
    existing_user = collection.find_one({"username": username})
    if existing_user:
        return jsonify({"message": "Username already exists"}), 409
    user = {
        "name": data["name"],
        "email": data["email"],
        "username": data["username"],
        "password": password
    }

    collection.insert_one(user)

    return jsonify({"message": "User registered successfully"})

# Login API
@app.route("/login", methods=["POST"])
def login():
    data = request.json

    user = collection.find_one({
        "username": data["username"],
        "password": data["password"]
    })

    if user:
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Incorrect username or password"}), 401

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json   

    num_robots = int(data["num_robots"])
    hour = int(data["hour"])
    num_days = int(data["num_days"])

    final_features = np.array([[num_robots, hour, num_days]])
    prediction = model2.predict(final_features)

    output = round(float(prediction[0]), 2)

    return jsonify({"prediction": output})  

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
