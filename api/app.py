import os
import pickle
import logging
from typing import Union
from flask import Flask, request
from flask_cors import CORS
from model import Model
from watchdog.events import FileSystemEventHandler
import time
import threading

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

app = Flask(__name__)
CORS(
    app,
    origins="*",
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

model: Union[Model, None] = None
MODEL_PATH = os.environ.get("MODEL_PATH")


def load_model(model_path):
    try:
        global model
        with open(model_path, "rb") as f:
            model = pickle.load(f)
        logging.info("Model loaded")
    except Exception as e:
        logging.error(f"Error loading model: {e}")


class ModelReloader(FileSystemEventHandler):
    def __init__(self, model_path):
        self.model_path = model_path

    def on_modified(self, event):
        if event.src_path == self.model_path:
            load_model(self.model_path)
            logging.info("Model reloaded")


def start_polling(model_path):
    last_modified_time = None
    while True:
        if os.path.exists(model_path):
            current_time = os.path.getmtime(model_path)
            if last_modified_time is None or current_time > last_modified_time:
                load_model(model_path)
                last_modified_time = current_time
        else:
            logging.warning("Model not found")
        time.sleep(5)


@app.route("/")
def helthcheck():
    return "OK\n", 200


@app.route("/api/recommend", methods=["POST"])
@app.route("/api/recommend/", methods=["POST"])
def recommend():
    if model == None:
        return "Model not found", 500

    data = request.get_json()
    x = set(data["songs"])
    recommendation = model.predict(x)

    response = {
        "songs": list(recommendation),
        "version": model.version,
        "model_date": model.fit_time,
    }

    return response, 200


if __name__ == "__main__":
    load_model(MODEL_PATH)

    watcher_thread = threading.Thread(target=start_polling, args=(MODEL_PATH,))
    watcher_thread.daemon = True
    watcher_thread.start()

    app.run(host="0.0.0.0")
