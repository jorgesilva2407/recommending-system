import os
import pickle
from flask import Flask, request
from model import Model

app = Flask(__name__)
model = None


@app.route("/")
def helthcheck():
    return "OK", 200


@app.route("/api/recommend", methods=["POST"])
def recommend():
    if model == None:
        return "Model not found", 500

    data = request.get_json()
    x = set(data["songs"])
    result = model.predict(x)

    return {"songs": list(result)}, 200


if __name__ == "__main__":
    PORT = os.environ.get("PORT", 5000)
    MODEL_PATH = os.environ.get("MODEL_PATH", "/app/model.pkl")

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)

    app.run(port=PORT)
