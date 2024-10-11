# app.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="../frontend/build", static_url_path="")
CORS(app)

counter = 0

@app.route("/counter", methods=["GET"])
def get_counter():
    global counter
    return jsonify({"counter": counter})

@app.route("/counter", methods=["POST"])
def increment_counter():
    global counter
    counter += 1
    return jsonify({"counter": counter})

# Serve React frontend
@app.route("/")
def serve_react_app():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
