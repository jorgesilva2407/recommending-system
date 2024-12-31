import os
import pickle
from flask import Flask, request
from flask_cors import CORS
from model import Model
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import threading

app = Flask(__name__)
CORS(
    app,
    origins="*",
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

model: Model | None = None
MODEL_PATH = os.environ.get("MODEL_PATH")


def load_model(model_path):
    global model
    with open(model_path, "rb") as f:
        model = pickle.load(f)


class ModelReloader(FileSystemEventHandler):
    def __init__(self, model_path):
        self.model_path = model_path

    def on_modified(self, event):
        if event.src_path == self.model_path:
            load_model(self.model_path)


def start_watcher(model_path):
    event_handler = ModelReloader(model_path)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(model_path), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


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
    try:
        load_model(MODEL_PATH)
    except Exception as e:
        print(e)

    watcher_thread = threading.Thread(target=start_watcher, args=(MODEL_PATH,))
    watcher_thread.daemon = True
    watcher_thread.start()

    app.run(host="0.0.0.0")
