import os
import sys
import re
import pickle
import datetime
import jwt
from functools import wraps
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path

# Add parent directory to sys.path for package imports
BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))

try:
    from api.db import collection
except ImportError:
    from db import collection

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

SECRET_KEY = os.environ.get("JWT_SECRET", "super-secret-jwt-key-2026")

MODEL_PATH = Path(__file__).parent.parent / "model.pkl"
model2 = pickle.load(open(MODEL_PATH, "rb"))

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]

        if not token:
            return jsonify({"message": "Token is missing! Please login again."}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.current_user = data["username"]
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token has expired! Please login again."}), 401
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid token! Please login again."}), 401

        return f(*args, **kwargs)
    return decorated

@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "message": "Backend server is active"})

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.json or {}
        username = data.get("username")
        password = data.get("password")
        name = data.get("name")
        email = data.get("email")

        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return jsonify({
                "message": "Password must contain at least one special character"
            }), 400

        existing_user = collection.find_one({"username": username})
        if existing_user:
            return jsonify({"message": "Username already exists"}), 409

        user = {
            "name": name,
            "email": email,
            "username": username,
            "password": password
        }

        collection.insert_one(user)

        return jsonify({"message": "User registered successfully"})
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500

# Login API with JWT token generation
@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.json or {}
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        user = collection.find_one({
            "username": username,
            "password": password
        })

        if user:
            # Generate JWT token valid for 24 hours
            exp_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
            token = jwt.encode(
                {"username": username, "exp": exp_time},
                SECRET_KEY,
                algorithm="HS256"
            )
            return jsonify({
                "message": "Login successful",
                "token": token
            })
        else:
            return jsonify({"message": "Incorrect username or password"}), 401
    except Exception as e:
        return jsonify({"message": f"Server error: {str(e)}"}), 500

# Protected Predict API
@app.route("/predict", methods=["POST"])
@token_required
def predict():
    try:
        data = request.json or {}
        num_robots = int(data["num_robots"])
        hour = int(data["hour"])
        num_days = int(data["num_days"])

        final_features = np.array([[num_robots, hour, num_days]])
        prediction = model2.predict(final_features)

        output = round(float(prediction[0]), 2)

        return jsonify({"prediction": output})  
    except Exception as e:
        return jsonify({"message": f"Prediction error: {str(e)}"}), 500

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"message": f"Server error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
