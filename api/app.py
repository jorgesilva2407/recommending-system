import os
import pickle
from flask import Flask, request
from flask_cors import CORS
from model import Model

app = Flask(__name__)
CORS(
    app,
    origins="*",  # Allow all origins or specify your React app's origin
    methods=["GET", "POST", "OPTIONS"],  # Explicitly allow OPTIONS
    allow_headers=["Content-Type"],  # Allow the Content-Type header
)
model = None


@app.route("/")
def helthcheck():
    return "OK", 200


@app.route("/api/recommend", methods=["POST"])
@app.route("/api/recommend/", methods=["POST"])
def recommend():
    if model == None:
        return "Model not found", 500

    data = request.get_json()
    x = set(data["songs"])
    result = model.predict(x)

    return {"songs": list(result)}, 200


if __name__ == "__main__":
    MODEL_PATH = os.environ.get("MODEL_PATH", "/app/model.pkl")

    with open(MODEL_PATH, "rb") as f:
        model: Model = pickle.load(f)

    app.run(host="0.0.0.0")
